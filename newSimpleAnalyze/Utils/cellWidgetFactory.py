from PyQt5.QtWidgets import QHBoxLayout, QPushButton, QWidget

class CellWidgetFactory:
    @staticmethod
    def create_cell_widget(row_index, table):
        cell_widget = QWidget()
        cell_layout = QHBoxLayout()

        cell_layout.setContentsMargins(0, 0, 0, 0)
        cell_layout.setSpacing(5)

        export_button = QPushButton("Export", cell_widget)
        export_button.setFixedSize(60, 21)
        CellWidgetFactory.connect_export_button(export_button, row_index, table)
        cell_layout.addWidget(export_button)

        flag_button = QPushButton("Flag", cell_widget)
        flag_button.setFixedSize(60, 21)
        CellWidgetFactory.connect_flag_button(flag_button, row_index, table)
        flag_button.setProperty('flagged', False)
        cell_layout.addWidget(flag_button)

        cell_widget.setLayout(cell_layout)
        return cell_widget

    @staticmethod
    def connect_export_button(button, row_index, table):
        button.clicked.connect(lambda: table.export_row(row_index))

    @staticmethod
    def connect_flag_button(button, row_index, table):
        button.clicked.connect(lambda: table.toggle_flag(button, row_index))