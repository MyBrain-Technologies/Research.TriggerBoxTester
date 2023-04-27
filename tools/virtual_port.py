import os
import serial
from serial.tools import list_ports

# Find available serial ports
ports = list_ports.comports()
for port in ports:
    print(port.device)

# Create virtual serial ports using the com0com tool
os.system('com0com\\setupc.exe /C=1 /B=9600')
ser1 = serial.Serial('COM3', baudrate=9600)
ser2 = serial.Serial('COM4', baudrate=9600)

# Print the names of the virtual serial ports
print("Virtual serial port 1:", ser1.portstr)
print("Virtual serial port 2:", ser2.portstr)

# Write data to one serial port and read it from the other
ser1.write(b'Hello, world!')
data = ser2.read_all()
print("Received data:", data)

# Close the serial ports
ser1.close()
ser2.close()

# Remove the virtual serial ports using the com0com tool
os.system('com0com\\setupc.exe /D=1')
