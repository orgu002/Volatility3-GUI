from PyQt5.QtWidgets import QMainWindow
from PyQt5.uic import  loadUi

class SettingsPage(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi('screens/settings.ui', self)
