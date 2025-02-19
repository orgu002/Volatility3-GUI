import sys

from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QApplication, QMainWindow, QStackedWidget, QPushButton
from screens.mainPage import MainPage
from screens.pluginScreen import PluginScreen
from screens.analyzeDataScreen import AnalyzeDataScreen
from screens.settingsPage import SettingsPage
from data.sessionManager import SessionManager
from Components.selectDump import SelectDump
from Components.runAnalysis import RunAnalysis
from Components.selectPlugin import SelectPlugin
from utils.fileUploader import FileUploader
from utils.chooseOs import ChooseOs
from data.plugins.pluginManager import PluginManager

class VolatilityApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Volatility App")
        self.setGeometry(100, 100, 800, 600)

        # Initialize session manager to store user state
        self.session_manager = SessionManager()
        self.session_manager.load_session()
        self.plugin_manager = PluginManager()
        self.select_dump = SelectDump()
        self.chooseOs = ChooseOs()
        self.select_plugin = SelectPlugin()
        self.file_uploader = FileUploader(self)
        self.run_analysis = RunAnalysis(self.select_dump, self.select_plugin)
        self.settings_screen = SettingsPage()
        self.select_file_screen = MainPage(self, self.file_uploader, self.chooseOs)
        self.plugin_screen = PluginScreen(self.plugin_manager, self.session_manager)
        self.analyzed_data_screen = AnalyzeDataScreen(select_dump=self.select_dump, select_plugin=self.select_plugin, file_uploader=self.file_uploader, run_analysis=self.run_analysis, export_manager=None, plugin_manager=self.plugin_manager)

        self.plugin_screen.plugins_updated.connect(self.select_plugin.set_plugins)
        self.file_uploader.file_path_updated.connect(self.select_dump.update_file_paths)
        self.select_dump.file_selected.connect(self.run_analysis.handle_selected_files)
        self.select_dump.file_selected.connect(self.analyzed_data_screen.update_file_label)
        self.select_plugin.plugin_selected.connect(self.analyzed_data_screen.update_plugin_label)
        self.chooseOs.os_changed.connect(self.plugin_manager.get_plugins)
        self.chooseOs.os_changed.connect(self.plugin_screen.load_plugins)

        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        self.stacked_widget.addWidget(self.select_file_screen)
        self.stacked_widget.addWidget(self.plugin_screen)
        self.stacked_widget.addWidget(self.analyzed_data_screen)
        self.stacked_widget.addWidget(self.settings_screen)

        select_file_action = QPushButton("Select File")
        select_file_action.clicked.connect(self.show_select_file_screen)

        plugins_action = QPushButton("Plugins")
        plugins_action.clicked.connect(self.show_plugin_screen)

        analyzed_data_action = QPushButton("Analyzed Data")
        analyzed_data_action.clicked.connect(self.show_analyzed_data_screen)

        settings_action = QPushButton("Settings")
        settings_action.clicked.connect(self.show_settings_screen)

        self.toolbar = self.addToolBar("Toolbar")
        self.toolbar.addWidget(select_file_action)
        self.toolbar.addWidget(plugins_action)
        self.toolbar.addWidget(analyzed_data_action)
        self.toolbar.addWidget(settings_action)

        # Setup connections for the run analysis process
        self.select_plugin.plugin_selected.connect(self.run_analysis.handle_selected_plugin)
        self.run_analysis.analysis_result.connect(self.analyzed_data_screen.display_data)

        # Set the files uploaded from previous session
        file_paths = self.session_manager.get_file_uploaded()
        if file_paths:
            for file_path in file_paths:
                self.select_file_screen.file_uploader.add_file_path(file_path)

        # Connect the file uploader signal to update file paths in SelectDump
        self.file_uploader.file_path_updated.connect(self.select_dump.update_file_paths)

        self.show()
        QTimer.singleShot(0, self.emit_initial_plugins)

    def show_select_file_screen(self):
        self.stacked_widget.setCurrentWidget(self.select_file_screen)

    def emit_initial_plugins(self):

        selected_plugins = self.session_manager.get_activated_plugins()
        self.plugin_screen.plugins_updated.emit(selected_plugins)

    def show_plugin_screen(self):
        self.stacked_widget.setCurrentWidget(self.plugin_screen)

    def show_analyzed_data_screen(self):
        self.stacked_widget.setCurrentWidget(self.analyzed_data_screen)

    def show_settings_screen(self):
        self.stacked_widget.setCurrentWidget(self.settings_screen)

    def update_analyzed_data(self, analyzed_result):
        self.analyzed_data_screen.display_data(analyzed_result)

    def update_selected_plugins(self, selected_plugins):
        print("Selected plugins:", selected_plugins)


    def closeEvent(self, event):
        self.session_manager.save_session()
        event.accept()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = VolatilityApp()
    window.show()
    sys.exit(app.exec_())
