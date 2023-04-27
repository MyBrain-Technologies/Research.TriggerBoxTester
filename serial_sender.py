from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QComboBox, QTextEdit, QPushButton, QSlider, QHBoxLayout, \
    QVBoxLayout, QCheckBox
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QIcon
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
        logo_label.setScaledContents(False)

        # Combobox to select serial port
        self.serial_combo = QComboBox()
        self.serial_combo.setMinimumWidth(120)
        self.serial_combo.setMaximumHeight(40)
        self.serial_combo.currentTextChanged.connect(self.serial_port_selected)
        self.refresh_serial_ports()

        # Add refresh button
        self.refresh_button = QPushButton(QIcon("assets/refresh.png"), "", self)
        self.refresh_button.setMaximumWidth(60)
        self.refresh_button.setMaximumHeight(40)
        self.refresh_button.setToolTip("Refresh serial ports list")
        self.refresh_button.move(360, 45)
        self.refresh_button.clicked.connect(self.refresh_serial_ports)

        # Add loop checkbox
        self.loop_message = QCheckBox()
        self.loop_message.setCheckState(False)
        self.loop_message.setToolTip("Check for looping the message")

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
        self.log_box.append("Welcome to the TriggerBox Tester, please select a serial port and start sending triggers.")
        self.log_box.append("Please select a serial port and start sending triggers.")
        self.log_box.append("Tip: write space separated values in the text box above.")
        self.log_box.repaint()

        # Layout
        hbox_refresh = QHBoxLayout()
        hbox_refresh.addWidget(self.serial_combo)
        hbox_refresh.addWidget(self.refresh_button)
        hbox_refresh.addWidget(QLabel("Loop message"))
        hbox_refresh.addWidget(self.loop_message)
        hbox_refresh.setAlignment(Qt.AlignLeft)

        hbox_logo = QHBoxLayout()
        hbox_logo.addWidget(logo_label)
        hbox_logo.setAlignment(Qt.AlignCenter)

        vbox = QVBoxLayout()
        vbox.addLayout(hbox_logo)
        vbox.addWidget(QLabel("Select Serial Port:"))
        vbox.addLayout(hbox_refresh)
        vbox.addWidget(QLabel("Triggers:"))
        vbox.addWidget(self.message_box)
        vbox.addWidget(self.send_button)
        vbox.addWidget(self.slider_label)
        vbox.addWidget(self.slider)
        vbox.addWidget(QLabel("Sent Messages:"))
        vbox.addWidget(self.log_box)
        vbox.addWidget(QLabel("© myBrainTechnologies - 2023"))

        self.setWindowTitle('MBT TriggerBox Tester')
        self.setLayout(vbox)

    def serial_port_selected(self):
        port_name = self.serial_combo.currentText()
        if self.serial_port and self.serial_port.isOpen():
            self.serial_port.close()
        try:
            self.serial_port = serial.Serial(port_name, 9600)
            self.serial_port.open()
            self.log_box.append("Selected serial port: " + port_name)
            self.log_box.repaint()
        except serial.SerialException as e:
            self.log_box.append(e)
            self.log_box.repaint()

    def refresh_serial_ports(self):
        self.serial_combo.clear()
        ports = [port.device for port in list_ports.comports()]
        for port, desc, hwid in sorted(ports):
            self.log_box.append("Found {}: {} [{}]".format(port, desc, hwid))
            self.log_box.repaint()
        self.serial_combo.addItems(ports)

    def send_message(self):

        message = self.message_box.toPlainText().replace('\n', '').strip()
        if message == 'dev':
            self.log_box.append("This tool was developed by Michele Romani.")
            self.log_box.repaint()
            return
        if not message:
            self.log_box.append("Write space separated characters in the text box to send them as triggers.")
            self.log_box.repaint()
            return

        if not self.serial_port or not self.serial_port.isOpen():
            self.log_box.append("You need to select a serial port.")
            self.log_box.repaint()
            return

        while self.loop_message.isChecked():
            for idx, char in enumerate(message):
                message_bytes = char.encode('utf-8')
                delay = self.slider.value()
                self.send_button.setEnabled(False)
                self.log_box.append("Encoding: " + char + " as " + str(message_bytes))
                self.log_box.repaint()
                self.log_box.append("Sending: " + str(message_bytes) + " with " + delay + "s intervals.")
                self.log_box.repaint()
                self.serial_port.write(message_bytes)
                time.sleep(delay)
        self.send_button.setEnabled(True)

    def slider_value_changed(self, value):
        self.slider_label.setText("Delay: {} sec".format(value))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = SerialSender()
    main_window.show()
    sys.exit(app.exec_())
