import sys

from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QLabel, QFileDialog, QMessageBox, QWidget, QPushButton, \
    QHBoxLayout
from PyQt5.uic import  loadUi
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QDragEnterEvent, QDropEvent, QPixmap
import os


class ChooseOs(QMainWindow):
    os_changed = pyqtSignal(str)

    def __init__(self, session_manager):
        super().__init__()
        try:
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")

        ui_path = os.path.join(base_path, 'ui', 'Os.ui')
        simple_analyze_logo = os.path.join(base_path, 'png', 'Simple Analyze.png')
        mnemonic_secondary_logo = os.path.join(base_path, 'png', 'mnemonic logo white 2.png')
        loadUi(ui_path, self)

        self.label.setPixmap(QPixmap(simple_analyze_logo))
        self.label_2.setPixmap(QPixmap(mnemonic_secondary_logo))

        self.session_manager = session_manager

        if self.session_manager.get_os() == "":
            self.session_manager.set_os("windows")


        self.on_os_changed(self.session_manager.get_os())

        if self.session_manager.get_os() == "windows":
            self.radioButtonWindows.setChecked(True)
        elif self.session_manager.get_os() == "linux":
            self.radioButtonLinux.setChecked(True)
        elif self.session_manager.get_os() == "mac":
            self.radioButtonMac.setChecked(True)

        self.radioButtonWindows.clicked.connect(lambda: self.on_os_changed("windows"))
        self.radioButtonMac.clicked.connect(lambda: self.on_os_changed("mac"))
        self.radioButtonLinux.clicked.connect(lambda: self.on_os_changed("linux"))

    def on_os_changed(self, text):
        print("Selected OS:", text)
        self.session_manager.set_os(text)
        self.os_changed.emit(text)







