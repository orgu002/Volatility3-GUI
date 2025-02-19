import os
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QSizePolicy, QFileDialog, QLabel, QProgressBar
from simpleAnalyze.Components.datatable import DataTable
from simpleAnalyze.Components.columnsSort import ColumnsSort
import xml.etree.ElementTree as ET

class AnalyzeDataScreen(QWidget):
    def __init__(self, file_uploader, select_dump, select_plugin, run_analysis, export_manager, plugin_manager):
        super().__init__()

        self.file_uploader = file_uploader
        self.select_dump = select_dump
        self.select_plugin = select_plugin
        self.run_analysis = run_analysis

        main_layout = QHBoxLayout(self)

        left_layout = QVBoxLayout()
        left_layout.setContentsMargins(0, 0, 0, 0)
        left_layout.setSpacing(0)

        header_layout = QHBoxLayout()

        self.select_dump.setFixedWidth(270)
        self.select_dump.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
        left_layout.addWidget(self.select_dump)

        self.select_plugin.setFixedWidth(270)
        self.select_plugin.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
        left_layout.addWidget(self.select_plugin)

        self.columns_button = QPushButton("Columns")
        self.columns_button.setFixedSize(100, 30)

        self.run_button = QPushButton("Run Analysis")
        self.run_button.setFixedWidth(270)
        self.run_button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        left_layout.addWidget(self.run_button)

        main_layout.addLayout(left_layout)

        right_layout = QVBoxLayout()

        labels_and_export_layout = QHBoxLayout()

        labels_layout = QVBoxLayout()
        self.file_label = QLabel("Selected File: None")
        self.plugin_label = QLabel("Selected Plugin: None")
        header_layout.addWidget(self.file_label)
        header_layout.addWidget(self.plugin_label)

        self.columns_sort = ColumnsSort()
        self.columns_sort.setFixedHeight(30)
        self.columns_sort.column_visibility_changed.connect(self.update_column_visibility)
        header_layout.addWidget(self.columns_sort, alignment=Qt.AlignTop)

        self.export_button = QPushButton("Export as...")
        self.export_button.setFixedHeight(30)
        self.export_button.clicked.connect(self.download_as_xml)
        header_layout.addWidget(self.export_button, alignment=Qt.AlignTop | Qt.AlignRight)

        self.show_flagged_button = QPushButton("Show Flagged Rows")
        self.show_flagged_button.setFixedWidth(150)
        self.show_flagged_button.setFixedHeight(30)
        self.show_flagged_button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        header_layout.addWidget(self.show_flagged_button, alignment=Qt.AlignTop | Qt.AlignRight)

        right_layout.addLayout(header_layout)

        self.data_table = DataTable()
        self.data_table.headers_updated.connect(self.update_columns_sort)
        right_layout.addWidget(self.data_table)

        self.loading_bar = QProgressBar()
        self.loading_bar.setRange(0, 100)
        self.loading_bar.setValue(0)
        right_layout.addWidget(self.loading_bar)

        main_layout.addLayout(right_layout)

        self.run_button.clicked.connect(self.start_analysis)
        self.show_flagged_button.clicked.connect(self.show_flagged_rows)

        self.reset_timer = QTimer(self)
        self.reset_timer.setSingleShot(True)
        self.reset_timer.timeout.connect(self.reset_progress_bar)

        self.original_button_text = self.run_button.text()

    def update_file_label(self, selected_files):
        if selected_files:
            self.file_label.setText(f"Selected File(s): {', '.join([os.path.basename(f[0]) for f in selected_files])}")
        else:
            self.file_label.setText("Selected File: None")

    def update_plugin_label(self, plugin_name):
        if plugin_name:
            self.plugin_label.setText(f"Selected Plugin: {plugin_name}")

    def display_data(self, data):
        self.data_table.update_table(data)

    def download_as_xml(self):
        data = self.data_table.get_data()

        if not data:
            return

        def sanitize_tag(tag):
            return ''.join(c if c.isalnum() or c == '_' else '_' for c in tag)

        root = ET.Element("Data")
        for item in data:
            record = ET.SubElement(root, "Record")
            for key, value in item.items():
                sanitized_key = sanitize_tag(key)
                field = ET.SubElement(record, sanitized_key)
                field.text = str(value)
        tree = ET.ElementTree(root)

        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getSaveFileName(self, "Save Data As", "", "XML Files (*.xml);;All Files (*)",
                                                   options=options)
        if file_name:
            tree.write(file_name, encoding='utf-8', xml_declaration=True)

    def update_column_visibility(self, column_name, is_visible):
        self.data_table.set_column_visibility(column_name, is_visible)

    def update_columns_sort(self, headers):
        self.columns_sort.update_columns(headers)

    def start_analysis(self):
        self.loading_bar.setValue(0)  # Reset loading bar
        self.update_button_text("Analyzing...")  # Update button text
        self.run_analysis.progress_updated.connect(self.update_progress)
        self.run_analysis.analysis_result.connect(self.analysis_complete)  # Connect analysis_complete slot
        self.run_analysis.run_analysis()

    def show_flagged_rows(self):
        self.data_table.show_flagged_rows()


    def update_progress(self, progress_percentage):
        self.loading_bar.setValue(progress_percentage)

    def analysis_complete(self):
        self.reset_timer.start(3000)
        self.update_button_text(self.original_button_text)

    def reset_progress_bar(self):
        self.loading_bar.setValue(0)

    def update_button_text(self, text):
        self.run_button.setText(text)

