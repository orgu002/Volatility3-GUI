import sys

from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QLabel, QFileDialog, QMessageBox, QWidget, QPushButton, \
    QHBoxLayout, QFrame
from PyQt5.uic import  loadUi
from PyQt5.QtCore import Qt, pyqtSignal, QSize
from PyQt5.QtGui import QDragEnterEvent, QDropEvent, QIcon, QFont, QPixmap
import os

from Utils.uploadConfirmation import is_valid_memory_dump, is_file_exists


# from simpleAnalyze.Utils.uploadConfirmation import is_valid_memory_dump, is_file_exists


class FileUploader(QMainWindow):
    file_path_updated = pyqtSignal(list)
    analyzedButtonClicked = pyqtSignal()

    def __init__(self):
        super().__init__()
        try:
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")

        ui_path = os.path.join(base_path, 'ui', 'FileUploader.ui')
        file_uploaded_img = os.path.join(base_path, 'png', 'Vector.png')
        self.close_icon = os.path.join(base_path, 'png', 'Close.png')
        loadUi(ui_path, self)

        self.label.setPixmap(QPixmap(file_uploaded_img))

        # available buttons:
        # self.selectButton
        # self.fileName
        # self.deleteBtn
        # self.analyzeButton
        # self.fileUploaded

        self.file_paths = []
        self.file_uploaded_label = None
        self.file_widgets = {}

        self.dropArea.setAcceptDrops(True)

        self.selectButton.clicked.connect(self.select_file)

        self.dropArea.dragEnterEvent = self.dragEnterEvent
        self.dropArea.dropEvent = self.dropEvent

        self.scroll_content_layout = QVBoxLayout()
        self.scroll_content_layout.setAlignment(Qt.AlignTop)
        self.scroll_content_layout.setSpacing(0)

        self.uploaded_layout = QVBoxLayout()
        self.uploaded_layout.setAlignment(Qt.AlignTop)
        self.uploaded_layout.setSpacing(0)

        self.fileUploaderScrollWidget = QWidget()
        self.fileUploaderScrollWidget.setLayout(self.scroll_content_layout)
        self.fileUploaderScroll.setWidget(self.fileUploaderScrollWidget)

        self.uploadedScrollWidget = QWidget()
        self.uploadedScrollWidget.setLayout(self.uploaded_layout)
        self.uploadedFilesScroll.setWidget(self.uploadedScrollWidget)

        self.uploaded_files_label = QLabel()
        self.uploaded_files_label.setAlignment(Qt.AlignCenter)
        self.uploaded_files_label.setFont(QFont('MS Shell Dlg 2', 10, QFont.Bold))
        self.uploaded_files_label.setStyleSheet("""
             QLabel {
                 color: white;
             }
         """)
        self.uploaded_layout.addWidget(self.uploaded_files_label)

    def dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event: QDropEvent):
        urls = event.mimeData().urls()
        if urls and urls[0].isLocalFile():
            file_path = urls[0].toLocalFile()
            if is_valid_memory_dump(file_path) and is_file_exists(file_path):
                self.add_file_path(file_path)
            else:
                QMessageBox.critical(self, "Error",
                                     "The file you selected is not a valid memory dump! Please select a valid file.\n(Supported file extensions: .vmem)")

    def select_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Memory Dump")
        if file_path:
            if is_valid_memory_dump(file_path) and is_file_exists(file_path):
                self.add_file_path(file_path)
            else:
                QMessageBox.critical(self, "Error",
                                     "The file you selected is not a valid memory dump! Please select a valid file.\n(Supported file extensions: .vmem)")

    def add_file_path(self, file_path):
        if file_path not in self.file_paths:
            self.file_paths.append(file_path)
            self.add_file_label(file_path)
            self.file_path_updated.emit(self.file_paths.copy())
            self.show_popup()
        else:
            print(f"File path {file_path} already exists in the list")

    def add_file_label(self, file_path):
        file_name = os.path.basename(file_path)
        print(f"Adding file label for: {file_name}")

        parentFrame = QFrame()

        frame1 = QFrame()
        frame2 = QFrame()

        label = QLabel(file_name)

        button = QPushButton()
        icon = QIcon(self.close_icon)
        button.setIcon(icon)
        button.setIconSize(QSize(16, 16))
        button.setCursor(Qt.PointingHandCursor)

        layout1 = QVBoxLayout()
        layout2 = QVBoxLayout()
        layout2.setAlignment(Qt.AlignLeft)

        layout1.addWidget(label)
        layout2.addWidget(button)

        frame1.setLayout(layout1)
        frame2.setLayout(layout2)

        layout1.setAlignment(Qt.AlignRight)

        parentLayout = QHBoxLayout()
        parentLayout.setContentsMargins(0, 0, 0, 0)
        parentLayout.addWidget(frame1)
        parentLayout.addWidget(frame2)

        parentFrame.setLayout(parentLayout)

        button.clicked.connect(lambda: self.delete_file(file_path))

        self.scroll_content_layout.addWidget(parentFrame)


    def show_popup(self):

        file_names = list(map(lambda file_path: os.path.basename(file_path), self.file_paths))

        # Group file names into rows of 5
        grouped_file_names = [", ".join(file_names[i:i + 5]) for i in range(0, len(file_names), 5)]
        formatted_file_names = "\n".join(grouped_file_names)

        # Set the formatted text to the uploaded files label
        if self.uploaded_files_label:
            self.uploaded_files_label.setText(formatted_file_names)

        if len(self.file_paths) == 1:
            analyze_button = QPushButton("Analyze My Data")
            analyze_button.setCursor(Qt.PointingHandCursor)
            analyze_button.setFont(QFont('MS Shell Dlg 2', 11, QFont.Bold))
            analyze_button.setMinimumSize(200, 30)
            analyze_button.setStyleSheet("""
                QPushButton {
                    background-color:#F27821;
                    color: white;
                    border: none;
                    border-radius: 5px;
                }
                QPushButton:hover {
                    background-color: #ff9933;
                }
            """)

            self.uploadedText.setText("Uploaded")

            self.analyzeButtonFrame.layout().addWidget(analyze_button)

            analyze_button.clicked.connect(self.emit_analyzeButtonClicked)

    def delete_file(self, file_path):
        if file_path in self.file_paths:
            self.file_paths.remove(file_path)
            if not self.file_paths:  # If file_paths list is empty
                self.uploadedText.setText("")
                self.delete_analyze_button()

        scroll_area_widget = self.fileUploaderScroll.widget()
        scroll_layout = scroll_area_widget.layout()

        for i in range(scroll_layout.count()):
            parent_frame = scroll_layout.itemAt(i).widget()
            if parent_frame:
                innerFrameLabel = parent_frame.layout().itemAt(0).widget()
                innerFrameButton = parent_frame.layout().itemAt(1).widget()
                if innerFrameLabel and innerFrameButton:
                    file_name_label = innerFrameLabel.layout().itemAt(0).widget()  # Access the label inside the inner frame
                    delete_button = innerFrameButton.layout().itemAt(0).widget()  # Access the delete button
                    if file_name_label and file_name_label.text() == os.path.basename(file_path):
                        delete_button.clicked.disconnect()  # Disconnect button signal
                        parent_frame.deleteLater()  # Delete the entire frame
                        self.update_uploaded_files_label()
                        break
        self.file_path_updated.emit(self.file_paths.copy())

    def update_uploaded_files_label(self):
        file_names = list(map(lambda file_path: os.path.basename(file_path), self.file_paths))
        file_name = ", ".join(file_names)
        self.uploaded_files_label.setText(file_name)


    def delete_analyze_button(self):
        analyze_button = self.analyzeButtonFrame.layout().itemAt(0).widget()
        if analyze_button:
            analyze_button.deleteLater()

    def emit_analyzeButtonClicked(self):
        self.analyzedButtonClicked.emit()

    def get_file_paths(self):
        return self.file_paths
