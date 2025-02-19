from PyQt5.QtWidgets import QPushButton, QMenu, QAction, QVBoxLayout, QWidget
from PyQt5.QtCore import pyqtSignal

class ColumnsSort(QWidget):
    column_visibility_changed = pyqtSignal(str, bool)

    def __init__(self):
        super().__init__()

        self.columns_button = QPushButton("Columns")
        self.columns_button.setFixedSize(100, 30)
        self.menu = QMenu()
        self.columns_button.setMenu(self.menu)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.addWidget(self.columns_button)

    def update_columns(self, headers):
        self.menu.clear()
        self.actions = {}
        for header in headers:
            action = QAction(header, self, checkable=True)
            action.setChecked(True)
            action.toggled.connect(lambda checked, hdr=header: self.column_visibility_changed.emit(hdr, checked))
            self.menu.addAction(action)
            self.actions[header] = action
