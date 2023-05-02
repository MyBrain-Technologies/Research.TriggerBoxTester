# Research.TriggerBoxTester
A simple Python application built with PyQT5 to test the TriggerBox developed by myBrainTechnologies.
The tool can be locally installed and run using Python on any OS, or through an executable available on the [release page](https://github.com/mbt-michele-r/Research.TriggerBoxTester/releases) (Windows only).
> **Warning**
> To access the serial ports of your system you need admin privileges.

## Usage
The tool assumes that you have access to MBT Acquisier App, with a protocol allowing activations (triggers) and a MBT EEG device. Futhermore, the MBT TriggerBox should be connected to both the PC and the EEG device.
The following devices are currently supported:
- Melomind
- Q+
- Hyperion

How to use the TriggerBoxTester:
- Open MBT TriggerBox Tester
- Select a Serial Port (On Windows it will be name COM + a number, on Unix systems it will be named ttyUSB + a number)
- Select an encoding (UTF-8 is the standard we use in myBrainTechnologies)
- Write some characters to be encoded
- Click on "Send Triggers"

There are some customizable options such as looping the sequence of triggers (still experimental and unstable) and setting the time delay between triggers (min 1 second, max 10 seconds).


## Prerequisites
Python 3.6 or higher
Pip package manager

## Installation
Clone the repository:

`git clone https://github.com/exampleuser/serial-sender.git`

`cd serial-sender`

Create a virtual environment:

`python -m venv venv`

Activate the virtual environment:

### On Windows:
`venv\Scripts\activate.bat`

### On macOS or Linux:
`source venv/bin/activate`

Install the required libraries:

`pip install -r requirements.txt`

Usage

To run the application, activate the virtual environment and run the serial_sender.py file:


## Activate the virtual environment (if not already activated)
### On Windows:

`venv\Scripts\activate.bat`

### On macOS or Linux:
`source venv/bin/activate`

### Run the application

`python serial_sender.py`

The application window should open, and you can select the serial port, enter the message, adjust the interval and checkbox settings, and send the message.

## Build executable
Currently only supported on Windows using [PyInstaller](https://pyinstaller.org) and [UPX](https://github.com/upx/upx).
### On Windows:
` pyinstaller  --name=MBTTriggerBoxTester --icon='assets\Icon.ico' --clean --splash="assets\splash.jpg" --upx-dir=upx --onefile --noconsole .\serial_sender.py ; copy -r "assets" "dist/"
`
