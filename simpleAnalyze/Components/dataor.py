def update_table(self, data):
    if not data:
        return

    # Parse data and color code
    all_rows_with_color = []
    for entry in data:
        color, rows_str = entry
        rows = [row.split('\t') for row in rows_str.strip().split('\n')[3:]]
        all_rows_with_color.extend([(row, color) for row in rows])

    # Set up model
    headers = daa[0][1].strip().split('\n')[2].split('\t')
    headers.insert(0, 'File')  # Add 'File' column as the first column
    headers.append('Edit/Export')
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

        # Add button for each row
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

        # Add color indicator based on provided color code
        color_indicator = QLabel("")
        color_indicator.setFixedSize(20, 20)
        color_indicator.setStyleSheet("background-color: {}".format(color))
        cell_layout.addWidget(color_indicator)

        cell_widget.setLayout(cell_layout)

        index = model.index(row_index, len(headers) - 1)  # Adjusted index for button column
        self.table_view.setIndexWidget(index, cell_widget)

    self.proxy_model.setSourceModel(model)

    # Set up table view properties
    self.table_view.horizontalHeader().setSectionResizeMode(QHeaderView.Fixed)
    self.table_view.verticalHeader().setSectionResizeMode(QHeaderView.Fixed)
    self.table_view.resizeColumnsToContents()
    self.table_view.setColumnWidth(0, 40)  # Adjusted column index for color column

    self.headers_updated.emit(headers)