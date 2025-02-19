from PyQt5.QtCore import QSortFilterProxyModel, QModelIndex

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

    def filterAcceptsRow(self, source_row, source_parent):
        search_text = self.filterRegExp().pattern().lower()
        model = self.sourceModel()
        for column in range(model.columnCount()):
            index = model.index(source_row, column, source_parent)
            data = model.data(index)
            if search_text in str(data).lower():
                return True
        return False
