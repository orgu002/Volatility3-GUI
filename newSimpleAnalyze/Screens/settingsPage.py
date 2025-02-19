import os
import sys

from PyQt5.QtWidgets import QMainWindow
from PyQt5.uic import  loadUi

class SettingsPage(QMainWindow):
    def __init__(self):
        super().__init__()
        try:
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")

        ui_path = os.path.join(base_path, 'ui', 'SettingsDark.ui')
        loadUi(ui_path, self)

        self.radioButtonDarkMode.toggled.connect(self.set_dark_mode)
        self.radioButtonLightMode.toggled.connect(self.set_light_mode)

    def set_dark_mode(self):
        if self.radioButtonDarkMode.isChecked():
            # Load the UI file for dark mode
            try:
                base_path = sys._MEIPASS
            except Exception:
                base_path = os.path.abspath(".")

            ui_path = os.path.join(base_path, 'ui', 'SettingsDark.ui')
            loadUi(ui_path, self)

            self.setStyleSheet("")  # Clear any existing stylesheet

            # Reconnect radio buttons to methods
            self.radioButtonDarkMode.toggled.connect(self.set_dark_mode)
            self.radioButtonLightMode.toggled.connect(self.set_light_mode)

    def set_light_mode(self):
        if self.radioButtonLightMode.isChecked():
            # Load the UI file for light mode
            try:
                base_path = sys._MEIPASS
            except Exception:
                base_path = os.path.abspath(".")

            ui_path = os.path.join(base_path, 'ui', 'SettingsLight.ui')
            loadUi(ui_path, self)
            self.setStyleSheet("")  # Clear any existing stylesheet

            # Reconnect radio buttons to methods
            self.radioButtonDarkMode.toggled.connect(self.set_dark_mode)
            self.radioButtonLightMode.toggled.connect(self.set_light_mode)