from PyQt5.QtCore import Qt, QModelIndex, pyqtSignal, QSortFilterProxyModel
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QTableView, QHeaderView, QPushButton, QLabel, QSizePolicy
from PyQt5.QtGui import QStandardItemModel, QStandardItem, QColor, QBrush
import xml.etree.ElementTree as ET

from simpleAnalyze.utils.exportmanager import ExportManager

class NumericSortFilterProxyModel(QSortFilterProxyModel):
    def lessThan(self, left: QModelIndex, right: QModelIndex) -> bool:
        left_data = self.sourceModel().data(left)
        right_data = self.sourceModel().data(right)

        if left_data is None or right_data is None:
            return False

        try:
            left_data = float(left_data)
            right_data = float(right_data)
        except ValueError:
            left_data = str(left_data)
            right_data = str(right_data)

        return left_data < right_data

class DataTable(QWidget):
    headers_updated = pyqtSignal(list)

    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        self.table_view = QTableView()
        layout.addWidget(self.table_view)
        self.setLayout(layout)

        self.proxy_model = NumericSortFilterProxyModel()
        self.table_view.setSortingEnabled(True)
        self.table_view.setModel(self.proxy_model)

        self.flagged_rows = set()
        self.showing_flagged = False  # Track if currently showing only flagged rows

    def update_table(self, data):
        if not data:
            return

        all_rows_with_color = self.parse_data(data)
        headers = self.setup_headers(data)
        model = self.setup_model(headers, all_rows_with_color)
        self.populate_table(model, headers, all_rows_with_color)
        self.setup_table_view(headers)
        self.headers_updated.emit(headers)

    def parse_data(self, data):
        all_rows_with_color = []
        for entry in data:
            color, rows_str = entry
            rows = [row.split('\t') for row in rows_str.strip().split('\n')[3:]]
            all_rows_with_color.extend([(row, color) for row in rows])
        return all_rows_with_color

    def setup_headers(self, data):
        headers = data[0][1].strip().split('\n')[2].split('\t')
        headers.insert(0, 'File')  # Add 'File' column as the first column
        headers.append('Edit/Export')
        return headers

    def setup_model(self, headers, all_rows_with_color):
        model = QStandardItemModel()
        model.setColumnCount(len(headers))
        model.setHorizontalHeaderLabels(headers)
        for row_index, (columns, color) in enumerate(all_rows_with_color):
            for col_index, value in enumerate(columns):
                item = QStandardItem(value)
                model.setItem(row_index, col_index + 1, item)  # Adjust column index

            # Add color to the color column (which is now at index 0)
            color_item = QStandardItem()
            color_item.setBackground(QColor(color))
            model.setItem(row_index, 0, color_item)  # Set color column at index 0
        return model

    def populate_table(self, model, headers, all_rows_with_color):
        self.proxy_model.setSourceModel(model)
        for row_index in range(len(all_rows_with_color)):
            cell_widget = self.create_cell_widget(row_index)
            index = model.index(row_index, len(headers) - 1)  # Adjusted index for button column
            self.table_view.setIndexWidget(self.proxy_model.mapFromSource(index), cell_widget)

    def create_cell_widget(self, row_index):
        cell_widget = QWidget()
        cell_layout = QHBoxLayout()
        cell_layout.setContentsMargins(0, 0, 0, 0)
        cell_layout.setSpacing(5)

        export_button = QPushButton("Export")
        export_button.setFixedSize(60, 21)
        export_button.clicked.connect(lambda _, row=row_index: self.export_row(row))
        cell_layout.addWidget(export_button)

        flag_button = QPushButton("Flag")
        flag_button.setFixedSize(60, 21)
        flag_button.clicked.connect(lambda _, button=flag_button, row=row_index: self.toggle_flag(button, row))
        flag_button.setProperty('flagged', False)
        cell_layout.addWidget(flag_button)

        cell_widget.setLayout(cell_layout)
        return cell_widget

    def setup_table_view(self, headers):
        self.table_view.horizontalHeader().setSectionResizeMode(QHeaderView.Fixed)
        self.table_view.verticalHeader().setSectionResizeMode(QHeaderView.Fixed)
        self.table_view.resizeColumnsToContents()
        self.table_view.setColumnWidth(0, 40)  # Adjusted column index for color column
        self.table_view.setColumnWidth(len(headers) - 1, 140)  # Adjusted column index for button column

        second_row_height = 50
        self.table_view.verticalHeader().resizeSection(1, second_row_height)
        self.table_view.verticalHeader().setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        for row in range(3):
            self.table_view.verticalHeader().hideSection(row)

    def get_data(self):
        model = self.proxy_model.sourceModel()
        if not model:
            return []

        data = []
        for row in range(3, model.rowCount()):
            row_data = {}
            for col in range(model.columnCount()):
                index = model.index(row, col)
                header = model.headerData(col, Qt.Horizontal)
                value = model.data(index)
                row_data[header] = value
            data.append(row_data)

        return data

    def set_column_visibility(self, column_name, is_visible):
        model = self.proxy_model.sourceModel()
        if not model:
            return

        for col in range(model.columnCount()):
            header = model.headerData(col, Qt.Horizontal)
            if header == column_name:
                self.table_view.setColumnHidden(col, not is_visible)
                break

    def export_row(self, row):
        model = self.proxy_model.sourceModel()
        if not model:
            return

        data = []
        for col in range(model.columnCount()):
            index = model.index(row, col)
            header = model.headerData(col, Qt.Horizontal)
            value = model.data(index)
            data.append({header: value})

        ExportManager.export_data(data, self)

    def toggle_flag(self, button, row):
        flagged = button.property('flagged')
        model = self.proxy_model.sourceModel()

        if not flagged:
            for col in range(1, model.columnCount()):
                index = model.index(row, col)
                item = model.itemFromIndex(index)
                item.setBackground(QColor("#FF6242"))
            self.flagged_rows.add(row)
            button.setStyleSheet("background-color: #ff6242; color: white; text-align: center;")
        else:
            for col in range(1, model.columnCount()):
                index = model.index(row, col)
                item = model.itemFromIndex(index)
                item.setBackground(QBrush())
            self.flagged_rows.remove(row)
            button.setStyleSheet("")

        button.setProperty('flagged', not flagged)

    def show_flagged_rows(self):
        self.showing_flagged = not self.showing_flagged  # Toggle the state
        model = self.proxy_model.sourceModel()
        if not model:
            return

        if self.showing_flagged:
            for row_index in range(model.rowCount()):
                self.table_view.setRowHidden(row_index, row_index not in self.flagged_rows)
        else:
            for row_index in range(model.rowCount()):
                self.table_view.setRowHidden(row_index, row_index < 3)  # Show all rows except the first three

