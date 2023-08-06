# spplot

This utility is a text mode implementation of what can be done in Arduino IDE
when choosing `Serial Plotter` option, i.e. it plots the numbers received on
the serial port in real time.

![](https://i.imgur.com/37MfwQr.png)

## spemu

There's also a helper utility included, called `spemu` which is a serial port
emulator. It's useful for testing when no real device is nearby.

#### Usage

Run `spemu`. The program will print file descriptor and PTY device path.
You can write directly to the `spemu` stdin or open file descriptor with some
script and write to it. The things you write will be outputted by the virtual
COM port.

## Installation

#### spplot

Install from PyPI:
```bash
python3 -m pip install spplot
```

Install locally:
```bash
python3 -m pip install . --upgrade
```

#### spemu

To compile it, just run `make`.

## Requirements

#### spplot

* Python 3 with f-strings
* POSIX-compliant, color-supporting terminal
* Font with Braille characters
* Modules from `requirements.txt`

#### spemu

* C compiler
* UNIX-like system

## Disclaimer: Work in Progress

This is a dirty draft of what I want it to be. I'll try to optimize it in my
free time and add some colors to differentiate the plots. As for now, it is
what it is.

The initial menu is made in TUI style but if you provide port and baudrate as
CLI args, you won't see it.

## Roadmap

- [ ] colored lines for different subplots
- [ ] total average / current buffer average and other stats
- [ ] better error handling
- [ ] buffer, display and calculation optimizations
- [ ] proper handling of negative values
- [x] set y axis range option
- [x] plot on n-th readout option
- [x] command line args
- [x] dynamic resizing
- [x] human menu keymapping
- [x] make a python package
- [x] make a PyPI release
