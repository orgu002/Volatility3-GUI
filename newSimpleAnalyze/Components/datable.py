from PyQt5.QtCore import Qt, pyqtSignal, QSortFilterProxyModel, QModelIndex
from PyQt5.QtGui import QColor, QBrush
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTableView, QSizePolicy

from Utils.dataParser import DataParser
from Utils.exportmanager import ExportManager
from Utils.headerManager import HeaderManager
from Utils.modelManager import ModelManager
from Utils.numericSortFilterProxyModel import NumericSortFilterProxyModel
from Utils.tablePopulator import TablePopulator
from Utils.tableViewConfigurator import TableViewConfigurator
from Utils.cellWidgetFactory import CellWidgetFactory

class NumericSortFilterProxyModel(QSortFilterProxyModel):
    def lessThan(self, left: QModelIndex, right: QModelIndex) -> bool:
        left_row = left.row()
        right_row = right.row()
        model = self.sourceModel()

        left_file_id = model.data(model.index(left_row, 0))
        right_file_id = model.data(model.index(right_row, 0))

        if left_file_id != right_file_id:
            return left_file_id < right_file_id

        left_value = model.data(left)
        right_value = model.data(right)

        try:
            left_value = float(left_value)
            right_value = float(right_value)
        except (ValueError, TypeError):
            left_value = str(left_value)
            right_value = str(right_value)

        return left_value < right_value


class DataTable(QWidget):
    headers_updated = pyqtSignal(list)

    def __init__(self):
        super().__init__()
        self.setup_ui()
        self.proxy_model = NumericSortFilterProxyModel()
        self.table_view.setSortingEnabled(True)
        self.table_view.setModel(self.proxy_model)
        self.flagged_rows = set()
        self.showing_flagged = False

    def setup_ui(self):
        layout = QVBoxLayout()
        self.table_view = QTableView()
        layout.addWidget(self.table_view)
        self.setLayout(layout)
        self.table_view.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

    def update_table(self, data):
        if not data:
            return

        all_rows_with_color = DataParser.parse_data(data)
        headers = HeaderManager.setup_headers(data)
        model = ModelManager.setup_model(headers, all_rows_with_color)
        TablePopulator.populate_table(self.table_view, self.proxy_model, model, headers, all_rows_with_color, self)
        TableViewConfigurator.setup_table_view(self.table_view, headers)
        self.headers_updated.emit(headers)

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

    def recreate_cell_widget(self):
        model = self.proxy_model.sourceModel()
        if not model:
            return
        headers = [model.headerData(col, Qt.Horizontal) for col in range(model.columnCount())]
        for row_index in range(model.rowCount()):
            cell_widget = CellWidgetFactory.create_cell_widget(row_index, self)
            index = model.index(row_index, len(headers) - 1)
            self.table_view.setIndexWidget(self.proxy_model.mapFromSource(index), cell_widget)

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
                self.table_view.setRowHidden(row_index, row_index < 3)