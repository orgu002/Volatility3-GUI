from PyQt5.QtWidgets import QHBoxLayout, QWidget, QVBoxLayout, QLabel, QCheckBox, QLineEdit, QSpacerItem, QSizePolicy
from PyQt5.QtCore import pyqtSignal, Qt

class PluginScreen(QWidget):
    plugins_updated = pyqtSignal(list)

    def __init__(self, plugin_manager, session_manager):
        super().__init__()
        self.plugins = []
        self.plugin_manager = plugin_manager
        self.session_manager = session_manager
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.setup_search_bar()
        os_type = "windows"
        self.load_plugins(os_type)

    def setup_search_bar(self):
        search_layout = QHBoxLayout()
        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("Search Plugins")
        search_layout.addWidget(self.search_bar)
        search_layout.addSpacerItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        self.layout.addLayout(search_layout)
        self.search_bar.textChanged.connect(self.populate_plugin_checkboxes)

    def load_plugins(self, os_type):
        self.plugins = self.plugin_manager.get_plugins(os_type)
        self.clear_layout()
        self.populate_plugin_checkboxes()

        selected_plugins = self.session_manager.get_activated_plugins()
        self.plugins_updated.emit(selected_plugins)

    def populate_plugin_checkboxes(self):
        self.clear_layout()
        search_text = self.search_bar.text()
        activated_plugins = set(self.session_manager.get_activated_plugins())
        for plugin in self.plugins:
            if search_text.lower() in plugin.name.lower():
                checkbox = QCheckBox(plugin.name)
                checkbox.clicked.connect(self.toggle_plugin)
                if plugin.name in activated_plugins:
                    checkbox.setChecked(True)
                self.layout.addWidget(checkbox)

        self.toggle_plugin()

    def toggle_plugin(self):
        selected_plugins = [checkbox.text() for checkbox in self.findChildren(QCheckBox) if checkbox.isChecked()]
        self.plugins_updated.emit(selected_plugins)
        self.session_manager.set_activated_plugins(selected_plugins)

    def clear_layout(self):
        for i in reversed(range(self.layout.count())):
            widget = self.layout.itemAt(i).widget()
            if widget is not None:
                widget.deleteLater()
