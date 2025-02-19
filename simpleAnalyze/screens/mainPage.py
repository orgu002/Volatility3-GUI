from PyQt5.QtWidgets import QWidget, QVBoxLayout, QFileDialog, QLabel
from PyQt5.QtCore import pyqtSignal
from simpleAnalyze.utils.fileUploader import FileUploader
from simpleAnalyze.utils.chooseOs import ChooseOs


class MainPage(QWidget):
    file_path_set = pyqtSignal(list)
    os_selected = pyqtSignal(str)

    def __init__(self, parent, file_uploader, chooseOs):
        super().__init__(parent)
        self.file_path = []
        layout = QVBoxLayout()

        self.file_uploader = file_uploader
        self.file_uploader.file_path_updated.connect(self.update_file_path)

        self.chooseOs = chooseOs
        self.chooseOs.os_changed.connect(self.os_selected)

        layout.addWidget(self.chooseOs)
        layout.addWidget(self.file_uploader)

        self.file_label = QLabel("No file selected")
        layout.addWidget(self.file_label)

        self.setLayout(layout)

    def update_file_path(self, file_paths):
        self.file_path = file_paths
        self.file_label.setText(f"Selected file(s): {', '.join(file_paths)}")
        self.file_path_set.emit(file_paths)

    def select_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Memory Dump")
        if file_path:
            self.update_file_path([file_path])
            self.file_uploader.add_file_path(file_path)  # Ensure FileUploader is aware of the selected file

    def on_os_selected(self, text):
        print("Selected OS:", text)
