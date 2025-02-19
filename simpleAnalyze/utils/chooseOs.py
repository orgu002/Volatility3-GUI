from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QFileDialog, QComboBox, QRadioButton
from PyQt5.QtCore import pyqtSignal

class ChooseOs(QWidget):
    os_changed = pyqtSignal(str)
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent_widget = parent

        self.layout = QVBoxLayout()
        self.on_os_changed("windows")

        self.windows_radio = QRadioButton('Windows')
        self.linux_radio = QRadioButton('Linux')
        self.mac_radio = QRadioButton('Mac')

        self.windows_radio.clicked.connect(lambda: self.on_os_changed("windows"))
        self.linux_radio.clicked.connect(lambda: self.on_os_changed("linux"))
        self.mac_radio.clicked.connect(lambda: self.on_os_changed("mac"))

        self.layout.addWidget(self.windows_radio)
        self.layout.addWidget(self.linux_radio)
        self.layout.addWidget(self.mac_radio)

        self.setLayout(self.layout)

        self.windows_radio.setChecked(True)


    def on_os_changed(self, text):
        print("Selected OS:", text)
        self.os_changed.emit(text)




