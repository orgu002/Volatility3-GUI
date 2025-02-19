import os
import sys
import xml.etree.ElementTree as ET
import csv
from PyQt5.QtCore import pyqtSignal, QSize
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (
    QMainWindow, QPushButton, QFrame, QFileDialog, QApplication, QHBoxLayout, QLineEdit, QMenu, QAction, QToolButton,
    QVBoxLayout, QWidget
)
from PyQt5.uic import loadUi

from Utils.exportmanager import ExportManager
from Components.datable import DataTable


class AnalyzeDataScreen(QMainWindow):
    """Main window for Data analysis."""

    def __init__(self, file_uploader, select_dump, select_plugin, run_analysis):
        """Initialize the AnalyzeDataScreen."""
        super().__init__()
        try:
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")

        ui_path = os.path.join(base_path, 'ui', 'DataAnalyze.ui')
        column_icon = os.path.join(base_path, 'png', 'Columns.png')
        export_icon = os.path.join(base_path, 'png', 'Export.png')
        loadUi(ui_path, self)

        self.columnsIcon.setIcon(QIcon(column_icon))
        self.columnsIcon.setIconSize(QSize(24, 24))

        self.exportIcon.setIcon(QIcon(export_icon))
        self.exportIcon.setIconSize(QSize(24, 24))

        # Load Components
        self.file_uploader = file_uploader
        self.select_dump = select_dump
        self.select_plugin = select_plugin
        self.run_analysis = run_analysis
        self.data_table = DataTable()

        # Set initial values
        self.labelFileChosenV.setText("None")
        self.labelPluginChosenV.setText("None")

        # Find frames
        self.frameDumps = self.findChild(QFrame, 'frameDumps')
        self.framePluginContent = self.findChild(QFrame, 'framePluginContent')
        self.frameDataContent = self.findChild(QFrame, 'frame_7')
        self.dataScroll = self.findChild(QFrame, 'dataScroll')
        self.dataScroll.setWidgetResizable(True)
        self.frame = self.findChild(QFrame, 'frame')
        self.runBtn = self.findChild(QPushButton, 'runBtn')
        self.frameTopRight = self.findChild(QFrame, 'frame_10')
        self.pluginsParentFrame = self.findChild(QFrame, 'frame_11')
        self.frameExport = self.findChild(QFrame, 'frameExport')
        self.frameColumns = self.findChild(QFrame, 'frameColumns')
        self.export_button = self.findChild(QPushButton, 'exportButton')
        self.flag_button = self.findChild(QPushButton,'exportButton_2')

        # Export buttons
        self.export_button.clicked.connect(self.export_data)
        self.exportIcon.clicked.connect(self.export_data)

        #Flag Button
        self.flag_button.clicked.connect(self.show_flagged_rows)

        # Data Table
        data_container = QWidget()
        data_layout = QVBoxLayout(data_container)
        data_layout.addWidget(self.data_table)
        self.dataScroll.setWidget(data_container)
        # add style to Data container
        data_container.setStyleSheet("""
            QWidget {
                background-color: #343534;
                color: #ffffff;  /* Change text color to white */
            }
            QTableWidget {
                background-color: #444444;  /* Change table background color */
                color: #ffffff;  /* Change table text color */
                gridline-color: #555555;  /* Change gridline color */
            }
            QHeaderView::section {
                background-color: #555555;  /* Change header background color */
                color: #ffffff;  /* Change header text color */
            }
            QTableWidget::item {
                background-color: #3a3a3a;  /* Change row background color */
            }
            QTableWidget::item:alternate {
                background-color: #2a2a2a;  /* Change alternate row background color */
            }
        """)

        # Columns sort
        self.menu = QMenu()
        self.columnsButton.setMenu(self.menu)
        self.columnsButton.setPopupMode(QToolButton.InstantPopup)

        self.menuIcon = QMenu()
        self.columnsIcon.setMenu(self.menuIcon)
        self.columnsIcon.setPopupMode(QToolButton.InstantPopup)

        # Filter when searching
        self.search_bar = self.findChild(QLineEdit, 'lineEditDataSearch')
        if self.search_bar is None:
            raise ValueError("Could not find the search bar widget. Please check the object name in the .ui file.")
        self.search_bar.setPlaceholderText("Search Data")
        self.search_bar.textChanged.connect(self.filter_data)

        # Retrieve existing layouts
        dump_layout = self.frameDumps.layout()
        plugin_layout = self.framePluginContent.layout()
        dump_layout.addWidget(self.select_dump)
        plugin_layout.addWidget(self.select_plugin)

        # Connect signals
        self.data_table.headers_updated.connect(self.update_columns_sort)
        self.runBtn.clicked.connect(self.start_analysis)

    def update_file_label(self, selected_files):
        """Update the file label with selected files."""
        if selected_files:
            file_names = [os.path.basename(file[0]) for file in selected_files]
            self.labelFileChosenV.setText(", ".join(file_names))

    def update_plugin_label(self, plugin_name):
        """Update the plugin label."""
        self.labelPluginChosenV.setText(plugin_name)

    def display_data(self, data):
        """Display Data in the Data table."""
        self.data_table.update_table(data)

    def export_data(self):
        """Export Data."""
        data = self.data_table.get_data()
        if not data:
            return
        ExportManager.export_data(data, self)

    def update_column_visibility(self, column_name, is_visible):
        """Update column visibility."""
        self.data_table.set_column_visibility(column_name, is_visible)

    def update_columns_sort(self, headers):
        """Update column sorting."""
        self.menu.clear()
        self.menuIcon.clear()

        for header in headers:
            action = QAction(header, self, checkable=True)
            action.setChecked(True)
            action.toggled.connect(lambda checked, hdr=header: self.update_column_visibility(hdr, checked))
            self.menu.addAction(action)
            self.menuIcon.addAction(action)

    def filter_data(self, text):
        self.data_table.proxy_model.setFilterRegExp(text)
        self.data_table.proxy_model.setFilterKeyColumn(-1)
        self.data_table.recreate_cell_widget()

    def start_analysis(self):
        """Start Data analysis."""
        self.run_analysis.run_analysis()

    def show_flagged_rows(self):
        self.data_table.show_flagged_rows()
