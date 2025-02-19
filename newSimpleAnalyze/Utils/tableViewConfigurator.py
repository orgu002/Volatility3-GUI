from PyQt5.QtWidgets import QHeaderView, QSizePolicy
from PyQt5.Qt import Qt

class TableViewConfigurator:
    @staticmethod
    def setup_table_view(table_view, headers):
        table_view.horizontalHeader().setSectionResizeMode(QHeaderView.Fixed)
        table_view.verticalHeader().setSectionResizeMode(QHeaderView.Fixed)
        table_view.resizeColumnsToContents()
        table_view.setColumnWidth(0, 40)  # Adjusted column index for color column
        table_view.setColumnWidth(len(headers) - 1, 140)  # Adjusted column index for button column

        second_row_height = 50
        table_view.verticalHeader().resizeSection(1, second_row_height)
        table_view.verticalHeader().setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        for row in range(3):
            table_view.verticalHeader().hideSection(row)

        table_view.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)  # Expand to fit the frame

