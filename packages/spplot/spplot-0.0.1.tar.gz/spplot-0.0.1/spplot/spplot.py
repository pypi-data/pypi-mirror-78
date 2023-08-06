#!/usr/bin/env python3

import sys
import termios
import time

from serial.tools.list_ports import comports

from .menu import Menu


OLD_TERM = termios.tcgetattr(sys.stdin.fileno())
BAUDRATES = [300, 2400, 9600, 19200, 38400, 57600, 115200, 230400]

def device_string(port, baud):
  dev = port.device
  desc = port.product
  return f'\x1b[38;5;4m{dev}\x1b[0m@\x1b[38;5;5m{baud}\x1b[0m ({desc})'

def warning(msg):
  goto(0, 0)
  print(
    f'\x1b[38;5;11mWARNING: {msg} [{time.perf_counter():.0f}]\x1b[0m',
    end='',
    flush=True
  )

def goto(x, y):
  print(f'\x1b[{y};{x}H', end='', flush=True)

def clear_screen():
  print('\x1b[2J', end='', flush=True)

def sigint_handler(*args):
  goto(0, 0)
  clear_screen()
  termios.tcsetattr(sys.stdin.fileno(), termios.TCSAFLUSH, OLD_TERM)
  sys.exit(0)

class CPort:
  product = 'User defined'

  def __init__(self, device):
    self.device = device

def find_port():
  cports = comports()
  ports = [p.device for p in cports]
  descs = [f'{p.product}' for p in cports]
  
  if not ports:
    print('No serial ports found.', file=sys.stderr)
    sys.exit(1)
  
  with Menu(ports, descriptions=descs, default_selection=0) as menu:
    port_i, port = menu.choose('Choose port:')
    cport = cports[port_i]

  return port, cport

def get_baud():
  with Menu(BAUDRATES, default_selection=BAUDRATES.index(115200)) as menu:
    _, baud = menu.choose('Choose baud rate:')
  return baud
