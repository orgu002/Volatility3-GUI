from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QVBoxLayout, QLabel, QWidget

class MainPage(QWidget):
    analyzedButtonClicked = pyqtSignal()
    file_path_updated = pyqtSignal(list)

    def __init__(self, file_uploader, os, session_manager):
        super().__init__()
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)

        self.os = os
        self.file_uploader = file_uploader
        self.session_manager = session_manager

        self.file_paths = self.session_manager.get_file_uploaded()

        self.file_uploader.analyzedButtonClicked.connect(self.on_analyze_button_clicked)
        self.file_uploader.file_path_updated.connect(self.on_file_path_updated)

        self.layout.addWidget(self.os)
        self.layout.addWidget(self.file_uploader)

        for file_path in self.file_paths:
            self.file_uploader.add_file_path(file_path)

    def on_analyze_button_clicked(self):
        self.analyzedButtonClicked.emit()

    def on_file_path_updated(self, file_paths):
        self.file_paths = file_paths
        self.file_path_updated.emit(file_paths)
        self.session_manager.set_file_uploaded(file_paths)
