from PyQt5.QtGui import QStandardItemModel, QStandardItem, QColor


class ModelManager:
    @staticmethod
    def setup_model(headers, all_rows_with_color):
        model = QStandardItemModel(len(all_rows_with_color), len(headers))
        model.setHorizontalHeaderLabels(headers)

        for row_idx, (row, color) in enumerate(all_rows_with_color):
            for col_idx, data in enumerate(row):
                item = QStandardItem(data)
                model.setItem(row_idx, col_idx, item)
            color_item = QStandardItem()
            color_item.setBackground(QColor(color))
            model.setItem(row_idx, 0, color_item)  # Set color item in the first column

        return model