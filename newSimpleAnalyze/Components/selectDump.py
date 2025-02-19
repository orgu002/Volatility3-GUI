import os
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QListWidget, QListWidgetItem, QCheckBox, QHBoxLayout
from PyQt5.QtCore import pyqtSignal, Qt

class SelectDump(QWidget):
    file_selected = pyqtSignal(list)

    def __init__(self):
        super().__init__()
        self.file_paths = []
        self.colors = [
            "#F89883",  # Light Salmon
            "#73C2FB",  # Sky Blue
            "#FDDD8D",  # Light Yellow
            "#90A4AE",  # Light Blue Gray
            "#C2E0CB",  # Light Green
            "#FFD9B3",  # Peach
            "#D9A7B0",  # Dusty Rose
            "#BDC3C7",  # Light Gray Blue
            "#C3E0E5",  # Pale Blue
            "#FFF0F5",  # Light Lavender
        ]
        self.color_index = 0
        self.setup_ui()
        self.apply_styles()

    def setup_ui(self):
        layout = QVBoxLayout()
        self.dump_list = QListWidget()
        layout.addWidget(self.dump_list)
        self.setLayout(layout)

    def update_file_paths(self, list_of_files):
        self.file_paths = list_of_files
        self.color_index = 0  # Reset color index when files change
        self.populate_file_list()
        print("Received file paths:", list_of_files)

    def apply_styles(self):
        self.dump_list.setStyleSheet("""
            QListWidget {
                border-radius: 5px;
                background-color: #343534;
                color: white;
                border: none;
            }
            QListWidget::item {
                color: white;
                height: 25px;
                border: none;
            }
        """)

    def populate_file_list(self):
        self.dump_list.clear()
        for file_path in self.file_paths:
            display_text = os.path.basename(file_path)
            color = self.colors[self.color_index % len(self.colors)]  # Use color index modulo list length
            self.add_list_item(display_text, file_path, color)
            self.color_index += 1  # Increment color index for next item

    def add_list_item(self, display_text, file_path, color):
        item = QListWidgetItem()
        layout = QHBoxLayout()
        layout.setContentsMargins(10, 10, 0, 0)
        layout.setSpacing(10)

        checkbox = QCheckBox()
        checkbox.stateChanged.connect(lambda state, fp=file_path, col=color: self.on_checkbox_state_changed(state, fp, col))
        checkbox.setStyleSheet("""
            QCheckBox::indicator {
                width: 10px;
                height: 10px;
                border-radius: 3px;
            }
            QCheckBox::indicator:unchecked {
                background-color: white;
                border: 1px solid #ccc;
            }
            QCheckBox::indicator:checked {
                background-color: #F27821;
                border: 1px solid #F27821;
            }
        """)
        layout.addWidget(checkbox)

        label = QLabel(display_text)
        label.setStyleSheet("color: white;")
        layout.addWidget(label)

        color_box = QLabel("")
        color_box.setFixedSize(10, 25)
        color_box.setStyleSheet(f"background-color: {color}; border-radius: 3px;")
        layout.addWidget(color_box)

        widget = QWidget()
        widget.setLayout(layout)
        item.setSizeHint(widget.sizeHint())
        item.setData(Qt.UserRole, (file_path, color))  # Store both file path and color in the item's Data
        layout.setSizeConstraint(QVBoxLayout.SetFixedSize)
        self.dump_list.addItem(item)
        self.dump_list.setItemWidget(item, widget)

    def on_checkbox_state_changed(self, state, file_path, color):
        selected_files = self.get_selected_files()
        self.file_selected.emit(selected_files)
        print(selected_files)

    def get_selected_files(self):
        selected_files = []
        for index in range(self.dump_list.count()):
            item = self.dump_list.item(index)
            widget = self.dump_list.itemWidget(item)
            checkbox = widget.findChild(QCheckBox)
            if checkbox.isChecked():
                file_path, color = item.data(Qt.UserRole)
                selected_files.append((file_path, color))  # Append tuple of file path and color
        return selected_files
