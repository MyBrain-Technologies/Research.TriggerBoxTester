from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QComboBox, QTextEdit, QPushButton, QSlider, QHBoxLayout, \
    QVBoxLayout
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from serial.tools import list_ports
import time
import serial
import sys


class SerialSender(QWidget):
    def __init__(self):
        super().__init__()


        self.serial_port = None


        # create a label for the logo
        logo_label = QLabel(self)
        logo_label.setPixmap(QPixmap("assets/logo.png"))
        logo_label.setScaledContents(True)
        logo_label.setGeometry(10, 10, 100, 100)

        # Combobox to select serial port
        self.serial_combo = QComboBox()
        self.serial_combo.currentTextChanged.connect(self.serial_port_selected)
        self.refresh_serial_ports()

        # Textbox for inputting message to send
        self.message_box = QTextEdit()
        self.message_box.setFixedHeight(60)
        self.message_box.setPlaceholderText("Enter comma triggers message here")

        # Button to send message
        self.send_button = QPushButton("Send Message")
        self.send_button.clicked.connect(self.send_message)

        # Slider to set message delay
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setMinimum(1)
        self.slider.setMaximum(10)
        self.slider.setTickPosition(QSlider.TicksBelow)
        self.slider.setTickInterval(1)
        self.slider.valueChanged.connect(self.slider_value_changed)
        self.slider_label = QLabel("Delay: {} sec".format(self.slider.value()))

        # Textbox for logging sent messages
        self.log_box = QTextEdit()
        self.log_box.setReadOnly(True)
        self.log_box.setStyleSheet("background-color: black; color: white")

        # Layout
        vbox = QVBoxLayout()
        vbox.addWidget(logo_label)
        vbox.addWidget(QLabel("Select Serial Port:"))
        vbox.addWidget(self.serial_combo)
        vbox.addWidget(QLabel("Message:"))
        vbox.addWidget(self.message_box)
        vbox.addWidget(self.send_button)
        vbox.addWidget(self.slider_label)
        vbox.addWidget(self.slider)
        vbox.addWidget(QLabel("Sent Messages:"))
        vbox.addWidget(self.log_box)

        self.setWindowTitle('MBT TriggerBox Tester')
        self.setLayout(vbox)

    def serial_port_selected(self):
        port_name = self.serial_combo.currentText()
        if self.serial_port and self.serial_port.isOpen():
            self.serial_port.close()
        try:
            self.serial_port = serial.Serial(port_name, 9600)
            self.log_box.append("Selected serial port: " + port_name)
            self.log_box.repaint()
        except serial.SerialException:
            pass

    def refresh_serial_ports(self):
        self.serial_combo.clear()
        ports = [port.device for port in list_ports.comports()]
        self.serial_combo.addItems(ports)

    def send_message(self):
        if not self.serial_port or not self.serial_port.isOpen():
            self.log_box.append("You need to select a serial port.")
            self.log_box.repaint()
            return
        message = self.message_box.toPlainText().replace('\n', '').strip()
        if not message:
            self.log_box.append("Write comma separated characters in the text box to send them as triggers.")
            self.log_box.repaint()
            return
        message_bytes = message.encode('ascii')
        delay = self.slider.value()
        self.send_button.setEnabled(False)
        self.log_box.append(message)
        self.log_box.repaint()
        if self.slider.value() == 1:
            self.serial_port.write(message_bytes)
        else:
            for byte in message_bytes:
                self.serial_port.write(bytes([byte]))
                time.sleep(delay)
        self.send_button.setEnabled(True)

    def slider_value_changed(self, value):
        self.slider_label.setText("Delay: {} sec".format(value))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = SerialSender()
    main_window.show()
    sys.exit(app.exec_())