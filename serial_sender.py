from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QComboBox, QTextEdit, QPushButton, QSlider, QHBoxLayout, \
    QVBoxLayout, QCheckBox
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QIcon
from serial.tools import list_ports
import time
import serial
import sys

try:
    with open("VERSION.txt", "r") as v:
        version = v.read().strip()
except:
    version = ''


class SerialSender(QWidget):
    def __init__(self):
        super().__init__()

        self.serial_port = None
        self.baudrate = 9600
        self.encoding = "utf-8"

        # create a label for the logo
        logo_label = QLabel(self)
        logo_label.setPixmap(QPixmap("assets/logo.png"))
        logo_label.setScaledContents(False)

        # Combobox to select serial port
        self.serial_combo = QComboBox()
        self.serial_combo.setMinimumWidth(120)
        self.serial_combo.setMaximumHeight(40)
        self.serial_combo.currentTextChanged.connect(self.serial_port_selected)

        # Combobox to select serial port
        self.encoding_combo = QComboBox()
        self.encoding_combo.setMinimumWidth(120)
        self.encoding_combo.setMaximumHeight(40)
        self.encoding_combo.addItems(['utf-8', 'ascii'])
        self.encoding_combo.currentTextChanged.connect(self.encoding_selected)

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
        self.loop_message.setToolTip("Check to send triggers in loop")

        # Textbox for inputting message to send
        self.message_box = QTextEdit()
        self.message_box.setFixedHeight(60)
        self.message_box.setPlaceholderText("Enter space separated triggers here")

        # Button to send message
        self.send_button = QPushButton("Send Trigger")
        self.send_button.clicked.connect(self.send_message)

        # Slider to set message delay
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setMinimum(1)
        self.slider.setMaximum(10)
        self.slider.setTickPosition(QSlider.TicksBelow)
        self.slider.setTickInterval(1)
        self.slider.valueChanged.connect(self.slider_value_changed)
        self.slider_label = QLabel("Delay between triggers: {} sec".format(self.slider.value()))

        # Textbox for logging sent messages
        self.log_box = QTextEdit()
        self.log_box.setReadOnly(True)
        self.log_box.setStyleSheet("background-color: black; color: white")
        self.log_box.append("Welcome to the MBT TriggerBox Tester v" + version)
        self.log_box.append("Please select a serial port and start sending triggers.")
        self.log_box.append("Tip: write space separated values in the text box above.")
        self.log_box.repaint()

        # Layout
        hbox_refresh = QHBoxLayout()
        hbox_refresh.addWidget(self.serial_combo)
        hbox_refresh.addWidget(self.refresh_button)
        hbox_refresh.addWidget(QLabel("Loop triggers"))
        hbox_refresh.addWidget(self.loop_message)
        hbox_refresh.addWidget(QLabel("Encoding"))
        hbox_refresh.addWidget(self.encoding_combo)
        hbox_refresh.setAlignment(Qt.AlignLeft)

        hbox_logo = QHBoxLayout()
        hbox_logo.addWidget(logo_label)
        hbox_logo.setAlignment(Qt.AlignCenter)

        hbox_bottom = QHBoxLayout()
        hbox_bottom.addWidget(QLabel("© myBrainTechnologies - 2023"))
        hbox_bottom.addWidget(QLabel("v" + version))

        vbox = QVBoxLayout()
        vbox.addLayout(hbox_logo)
        vbox.addWidget(QLabel("Select Serial Port:"))
        vbox.addLayout(hbox_refresh)
        vbox.addWidget(QLabel("Triggers:"))
        vbox.addWidget(self.message_box)
        vbox.addWidget(self.send_button)
        vbox.addWidget(self.slider_label)
        vbox.addWidget(self.slider)
        vbox.addWidget(QLabel("Activity logs:"))
        vbox.addWidget(self.log_box)
        vbox.addLayout(hbox_bottom)

        self.setWindowTitle('MBT TriggerBox Tester')
        self.setLayout(vbox)
        self.refresh_serial_ports()

    def serial_port_selected(self):
        """
        Set the selected serial port and updates the log box.
        """
        port_name = self.serial_combo.currentText()
        if self.serial_port and self.serial_port.isOpen():
            self.serial_port.close()
        try:
            self.serial_port = serial.Serial(port=port_name, baudrate=self.baudrate)
            if not self.serial_port.isOpen():
                self.serial_port.open()
            self.log_box.append("Selected serial port: " + port_name)
            self.log_box.repaint()
        except serial.SerialException as e:
            self.log_box.append("Cannot open the serial ports: " + str(e))
            self.log_box.repaint()

    def encoding_selected(self):
        """
        Set the selected encoding standard port and updates the log box.
        """
        self.encoding = self.encoding_combo.currentText()
        self.log_box.append("Selected encoding: " + self.encoding)
        self.log_box.repaint()

    def refresh_serial_ports(self):
        """
        Scan the system for available serial ports and updates the dropdown menu
        """
        self.serial_combo.clear()
        self.log_box.append("Scanning for serial ports...")
        self.log_box.repaint()
        try:
            ports = [port.device for port in list_ports.comports()]
            self.log_box.append(str(ports))
            for port in sorted(ports):
                self.log_box.append("Found: {}".format(port))
                self.log_box.repaint()
            self.serial_combo.addItems(ports)
            self.serial_port = serial.Serial(port=ports[0], baudrate=self.baudrate)
        except serial.SerialException as e:
            self.log_box.append("Error while scanning the serial ports: " + str(e))
            self.log_box.repaint()

    def send_message(self):
        """
        Parse the input box and sends each character encoded as a byte string
        """
        message = self.message_box.toPlainText().replace('\n', '').replace(" ", "").strip()
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

        self.send_button.setEnabled(False)
        self.encode_and_send(message=message)

        while self.loop_message.isChecked():
            self.encode_and_send(message=message)
        self.send_button.setEnabled(True)

    def encode_and_send(self, message):
        for idx, char in enumerate(message):
            message_bytes = char.encode(self.encoding)
            delay = self.slider.value()
            self.log_box.append("Encoding: " + char + " as " + str(message_bytes))
            self.log_box.repaint()
            self.log_box.append("Sending: " + str(message_bytes) + " with " + str(delay) + "s intervals.")
            self.log_box.repaint()
            self.serial_port.write(message_bytes)
            time.sleep(delay)

    def slider_value_changed(self, value):
        self.slider_label.setText("Delay between triggers: {} sec".format(value))


if __name__ == '__main__':
    try:
        import pyi_splash

        pyi_splash.update_text('UI Loaded ...')
        pyi_splash.close()
    except:
        pass
    app = QApplication(sys.argv)
    main_window = SerialSender()
    main_window.show()
    sys.exit(app.exec_())
