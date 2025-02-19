import os
import sys
from PyQt5.QtCore import pyqtSignal, QTimer, QSize
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QMainWindow, QStackedWidget
from Screens.mainPage import MainPage
from Screens.analyzeDataScreen import AnalyzeDataScreen
from Components.fileUploader import FileUploader
from Components.chooseOs import ChooseOs
from Screens.pluginScreen import PluginScreen
from Screens.settingsPage import SettingsPage
from Components.selectDump import SelectDump
from Components.runAnalysis import RunAnalysis
from Components.selectPlugin import SelectPlugin
from PyQt5.uic import loadUi
from Data.sessionManager import SessionManager

basedir = os.path.dirname(__file__)

try:
    from ctypes import windll
    myappid = 'mnemonic.simpleanalyze.data.1'
    windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
except ImportError:
    pass

class VolatilityApp(QMainWindow):
    activeCommandsUpdated = pyqtSignal(list)
    file_path_updated = pyqtSignal(list)
    os_changed = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        try:
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")

        ui_path = os.path.join(base_path, 'ui', 'NavigationBar.ui')
        settings_icon = os.path.join(base_path, 'png', 'settings.png')
        menomic_logo = os.path.join(base_path, 'png', 'Mnemonic logo.png')

        loadUi(ui_path, self)
        self.setWindowTitle("Simple analyze")

        self.settingsBtn.setIcon(QIcon(settings_icon))
        self.settingsBtn.setIconSize(QSize(50, 50))

        self.mainBtn.setIcon(QIcon(menomic_logo))
        self.settingsBtn.setIconSize(QSize(100, 100))

        # Initialize Components and session manager
        self.session_manager = SessionManager()
        self.file_uploader = FileUploader()
        self.os = ChooseOs(self.session_manager)
        self.select_dump = SelectDump()
        self.select_plugin = SelectPlugin()
        self.run_analysis = RunAnalysis(self.select_dump, self.select_plugin)

        # Initialize Screens
        self.main_page = MainPage(self.file_uploader, self.os, self.session_manager)
        self.plugins_page = PluginScreen(self.session_manager, self.os.os_changed)
        self.data_page = AnalyzeDataScreen(self.file_uploader, self.select_dump, self.select_plugin, self.run_analysis)
        self.settings_page = SettingsPage()

        # Connect signals and slots
        self.plugins_page.activeCommandsUpdated.connect(self.select_plugin.set_plugins)
        self.file_uploader.file_path_updated.connect(self.select_dump.update_file_paths)
        self.select_dump.file_selected.connect(self.run_analysis.handle_selected_files)
        self.select_dump.file_selected.connect(self.data_page.update_file_label)
        self.select_plugin.plugin_selected.connect(self.data_page.update_plugin_label)
        self.select_plugin.plugin_selected.connect(self.run_analysis.handle_selected_plugin)
        self.run_analysis.analysis_result.connect(self.data_page.display_data)

        # Add Screens to the stacked widget
        self.stackedWidget.addWidget(self.main_page)
        self.stackedWidget.addWidget(self.data_page)
        self.stackedWidget.addWidget(self.plugins_page)
        self.stackedWidget.addWidget(self.settings_page)

        # Connect navigation buttons to screen switch functions
        self.mainBtn.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.main_page))
        self.dataBtn.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.data_page))
        self.pluginsBtn.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.plugins_page))
        self.settingsBtn.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.settings_page))

        self.main_page.file_path_updated.connect(self.file_path_updated.emit)
        self.main_page.analyzedButtonClicked.connect(self.switch_to_data_page)

        # Load previously uploaded files and activated plugins
        file_paths = self.session_manager.get_file_uploaded()
        if file_paths:
            for file_path in file_paths:
                self.file_uploader.add_file_path(file_path)


        QTimer.singleShot(0, self.emit_initial_plugins_and_files)

    def switch_to_data_page(self):
        self.stackedWidget.setCurrentWidget(self.data_page)

    def on_active_commands_updated(self, active_commands):
        print(f"Received active commands update: {active_commands}")
        self.activeCommandsUpdated.emit(active_commands)

    def emit_initial_plugins_and_files(self):
        # Emit signal to load plugins from previous session
        activated_plugins = self.session_manager.get_activated_plugins()
        if activated_plugins:
            self.plugins_page.activeCommandsUpdated.emit(activated_plugins)

        # Emit signal to update file paths in SelectDump
        file_paths = self.session_manager.get_file_uploaded()
        if file_paths:
            self.file_uploader.file_path_updated.emit(file_paths)

    def closeEvent(self, event):
        # Save session before closing
        self.session_manager.save_session()
        event.accept()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon(os.path.join(basedir, 'ico', 'mnemonic.ico')))
    window = VolatilityApp()
    window.show()
    sys.exit(app.exec_())
