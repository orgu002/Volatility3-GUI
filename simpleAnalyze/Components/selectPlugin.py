from PyQt5.QtWidgets import QWidget, QVBoxLayout, QGroupBox, QListWidget, QListWidgetItem, QLabel
from PyQt5.QtCore import Qt, pyqtSignal

class SelectPlugin(QWidget):
    plugin_selected = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.plugins = []
        self.plugins_group = QGroupBox("PLUGINS")
        self.plugins_layout = QVBoxLayout()
        self.plugins_header = QLabel("PLUGINS")
        self.plugins_subheader = QLabel("Choose a plugin to analyze memory dump")
        self.plugins_list = QListWidget()
        self.apply_styles()

        self.plugins_layout.addWidget(self.plugins_header)
        self.plugins_layout.addWidget(self.plugins_subheader)
        self.plugins_layout.addWidget(self.plugins_list)
        self.plugins_group.setLayout(self.plugins_layout)

        self.setLayout(self.plugins_group.layout())

    def set_plugins(self, plugins):
        print("Plugins: ", plugins)
        self.plugins = plugins
        self.populate_plugins_list()

    def populate_plugins_list(self):
        self.plugins_list.clear()
        for plugin in self.plugins:
            item = QListWidgetItem(plugin)
            item.setFlags(item.flags() | Qt.ItemIsUserCheckable)
            item.setCheckState(Qt.Unchecked)  # Ensure plugins are not checked by default
            item.setData(Qt.UserRole, plugin)
            self.plugins_list.addItem(item)
            self.plugins_list.itemChanged.connect(self.plugin_selection_changed)

    def plugin_selection_changed(self, item):
        if item.checkState() == Qt.Checked:
            selected_plugin = item.data(Qt.UserRole)
            self.plugin_selected.emit(selected_plugin)
            if selected_plugin:
                for index in range(self.plugins_list.count()):
                    if self.plugins_list.item(index) is not item:
                        self.plugins_list.item(index).setCheckState(Qt.Unchecked)

    def apply_styles(self):
        self.plugins_header.setStyleSheet("""
            color:#FFFFFF;
            font-size: 18px;
            padding: 0px;
            border: none;
            border-bottom: 1px solid #F27821;
        """)
        self.plugins_subheader.setStyleSheet("""
            color: #FFFFFF;
            font-size: 9px;
        """)
        self.plugins_list.setStyleSheet("""
            QListWidget {
                border-radius: 5px;
                background-color: #343534;
                color: white;
                border: none;
                padding: 0px;
            }

            QListWidget::item {
                color: white;
                height: 25px;
                padding: 5px;
                border: none;
                background-color: #343534;
            }

            QCheckbox::indicator {
                width: 10px;
                height: 10px;
                border-radius: 3px;
            }

            QListWidget::indicator:unchecked {
                background-color: white;
                border: 1px solid #ccc;
            }

            QListWidget::indicator:checked {
                background-color: #F27821;
                border: 1px solid #F27821;
            }
        """)
