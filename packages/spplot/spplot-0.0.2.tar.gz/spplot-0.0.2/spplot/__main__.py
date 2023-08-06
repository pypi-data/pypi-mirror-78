import argparse
import math
import serial
import shutil
import signal

from drawille import Canvas

from .spplot import *
from .meta import NAME, DESC, VERSION


def main():
  signal.signal(signal.SIGINT, sigint_handler)

  parser = argparse.ArgumentParser(NAME, description=DESC)
  parser.add_argument('-b', '--baud', type=str, help='baud rate')
  parser.add_argument('-p', '--port', type=str, help='serial port device')
  parser.add_argument('-t', '--timeout', type=float, help='"no data" warning timeout', default=5.0)
  parser.add_argument('-f', '--framerate', type=int, help='display update on every Nth readout', default=1)
  parser.add_argument('-v', '--version', action='store_true', help='display version')
  parser.add_argument('-y', '--y-min', type=float, help='y axis minimum', default=0.0)
  parser.add_argument('-Y', '--y-max', type=float, help='y axis maximum')
  args = parser.parse_args()

  if args.version:
    print(f'{NAME} v.{VERSION}')
    sys.exit(0)

  port, cport = (args.port, CPort(args.port)) if args.port else find_port()
  baud = args.baud if args.baud else get_baud()

  buf = ['0']
  cvs = Canvas()
  s = serial.Serial(port, baud, timeout=args.timeout)
  frame_counter = 0
  print('Opening', device_string(cport, baud))
  ymin, ymax = args.y_min, args.y_max

  while True:
    w, h = shutil.get_terminal_size((80, 24))
    
    try:
      line = s.readline().decode('ascii').strip()
    except UnicodeDecodeError:
      continue
    except serial.SerialException:
      error('Serial connection broke')
      break

    if line == '':
      warning('no data')
      continue
    else:
      buf.append(line)

    # Shift the data
    if len(buf) >= w*2:
      buf = buf[-w*2:]
    
    # A list of all numbers from all plots in the buffer
    try:
      nums = sum([[float(x) for x in l.split(' ')] for l in buf], [])
    except ValueError:
      warning('NaN data')
      del buf[-1]
      time.sleep(0.5)
      continue

    if ymax:
      maxnum = ymax * 1.1
    else:
      maxnum = max(nums) * 1.1
    minnum = min(nums)

    # Plot the Braille lines
    frame_counter += 1
    if frame_counter % args.framerate == 0:
        goto(0, 0)
        clear_screen()
        cvs.clear()
        
        cvs.set(0, normalize(ymin, h, maxnum))
        cvs.set(0, normalize(maxnum, h, maxnum))

        for i, l in enumerate(buf):
          l = [float(x) for x in l.split(' ')]
          for j, x in enumerate(l):
            # normalized value (adjusted to tty height)
            # h*4 because there are 4 Braille dots per row
            if ymin <= x <= (ymax if ymax else math.inf):
              cvs.set(i, normalize(x, h, maxnum))
        print(cvs.frame())

        # Attach some information
        print(f'{ymin:.1f}')
        print(device_string(cport, baud))
        print(f'{line}')
        print(f'\x1b[0;0H{ymax if ymax else maxnum:.1f}', end='', flush=True)

  s.close()

if __name__ == '__main__':
  main()
