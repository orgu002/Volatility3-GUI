from PyQt5.Qt import Qt
from Utils.cellWidgetFactory import CellWidgetFactory

class TablePopulator:
    @staticmethod
    def populate_table(table_view, proxy_model, model, headers, all_rows_with_color, data_table):
        proxy_model.setSourceModel(model)
        for row_index in range(len(all_rows_with_color)):
            cell_widget = CellWidgetFactory.create_cell_widget(row_index, data_table)
            index = model.index(row_index, len(headers) - 1)  # Adjusted index for button column
            table_view.setIndexWidget(proxy_model.mapFromSource(index), cell_widget)

    @staticmethod
    def recreate_cell_widget(table_view, proxy_model):
        model = proxy_model.sourceModel()
        if not model:
            return
        headers = [model.headerData(col, Qt.Horizontal) for col in range(model.columnCount())]
        for row_index in range(model.rowCount()):
            cell_widget = CellWidgetFactory.create_cell_widget(row_index, table_view)
            index = model.index(row_index, len(headers) - 1)
            table_view.setIndexWidget(proxy_model.mapFromSource(index), cell_widget)