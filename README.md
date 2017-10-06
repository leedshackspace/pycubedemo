# 3D cube demo patterns

## What is this?

This repository contains demo patterns for a 3D cube written in Python. It supports both an internal OpenGL renderer, and driving an external LED cube, either over a serial connection or a network.

The code should run fine under both Python 2.7 and Python 3.

## Dependencies / Setup

The Python package `numpy` is required, and if you want to use the OpenGL renderer, also `pygame` and `pyopengl`. These can be installed in various ways depending on your OS.

### Debian-like (inc. Ubuntu) Linux

`sudo apt-get install python-numpy python-pygame python-opengl`

### Mac OS X / Other

`pip install -r requirements.txt`

## Running

### Demo patterns

`python cube.py`

Run the cube demo patterns using the default OpenGL renderer. It will cycle through all patterns in a random order.

### Run a particular pattern

Add `--pattern <name>`, where `<name>` is the name of the pattern to run. Run a set of patterns by using a comma-separated list of names.

### Connect to an external cube/simulator

Add `--port hostname:portnum`.

Examples:

`--port 192.168.0.6:5000`

`--port /dev/ttyUSB0`

## Developing patterns

New patterns can be added by by placing a new Python file in the `patterns/` directory, which implements the `Pattern` class. The `init` function is called when the pattern is started. It should return the delay between frames in milliseconds. For every frame the `tick` function is called.

The image is set using `self.cube.clear` and `self.cube.set_pixel`. To avoid flickering, double buffering can be enabled with `self.double_buffer = True`.

The easiest way to get started is to copy and modify an existing pattern. `fade` and `wave` are probably good starting points.

## Problems installing pygame

Installing pygame on a Mac is apparently much harder than it should be. Mac users may be interested in the Node.js/WebGL browser-based cube emulator at https://github.com/ultrafez/ledcube-webgl
