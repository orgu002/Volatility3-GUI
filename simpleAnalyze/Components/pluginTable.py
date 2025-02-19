import sys
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QSizePolicy


class PluginTable(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent_widget = parent

        self.layout = QVBoxLayout()

        self.table_widget = QTableWidget()
        self.table_widget.setRowCount(4)
        self.table_widget.setColumnCount(1)

        self.table_widget.setItem(0, 0, QTableWidgetItem("Test1"))
        self.table_widget.setItem(1, 0, QTableWidgetItem("Test2"))
        self.table_widget.setItem(2, 0, QTableWidgetItem("Test3"))
        self.table_widget.setItem(3, 0, QTableWidgetItem("Test4"))

        self.table_widget.verticalHeader().setVisible(False)
        self.table_widget.horizontalHeader().setVisible(False)

        self.table_widget.setAlternatingRowColors(True)

        self.layout.addWidget(self.table_widget)

        self.layout.setContentsMargins(0, 0, 0, 0)
        self.table_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.setLayout(self.layout)

