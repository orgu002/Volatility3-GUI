import os
import sys

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QMainWindow, QFrame, QHBoxLayout, QLineEdit, QScrollArea, QToolTip, QApplication
from PyQt5.QtCore import pyqtSignal, Qt, QEvent, QPoint
from PyQt5.uic import loadUi
from Components.py_toggle import PyToggle
from Data.plugins.pluginManager import PluginManager

class PluginScreen(QMainWindow):
    plugins_updated = pyqtSignal(list)
    activeCommandsUpdated = pyqtSignal(list)

    def __init__(self, session_manager, choose_os):
        super().__init__()
        try:
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")

        ui_path = os.path.join(base_path, 'ui', 'Plugins.ui')
        loadUi(ui_path, self)

        QApplication.instance().setStyleSheet("QToolTip { background-color: black; color: white; border: 1px solid white; padding: 5px; font-size: 10pt; }")

        self.session_manager = session_manager
        self.activeCommands = self.session_manager.get_activated_plugins()
        self.os = session_manager.get_os()

        self.scroll_layout = QVBoxLayout()
        self.scroll_layout.setSpacing(5)
        self.scroll_layout.setContentsMargins(20, 0, 20, 0)
        self.scroll_layout.setSizeConstraint(QVBoxLayout.SetMinimumSize)

        widget = QWidget()
        widget.setLayout(self.scroll_layout)


        self.pluginScroll.setWidget(widget)
        self.pluginScroll.setWidgetResizable(True)
        self.pluginScroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)

        self.is_searching = False

        self.plugins_data = PluginManager()
        self.search_bar = self.findChild(QLineEdit, 'lineEditPluginSearch')
        if self.search_bar is None:
            raise ValueError("Could not find the search bar widget. Please check the object name in the .ui file.")
        self.search_bar.setPlaceholderText("Search Plugins")
        self.search_bar.textChanged.connect(self.populate_plugin_toggles)

        choose_os.connect(self.change_plugin_os)

        self.plugins = self.plugins_data.get_plugins(self.os)
        self.populate_plugin_toggles()

    def create_plugin_toggle(self, plugin_name, plugin_description, color):
        firstFrame = QFrame()
        firstFrame.setFixedHeight(50)

        layout = QHBoxLayout()

        label = QLabel(plugin_name)
        label.setStyleSheet("color:white;")
        label.setToolTip(plugin_description)
        label.installEventFilter(self)
        layout.addWidget(label)

        toggle = PyToggle()
        layout.addWidget(toggle)
        layout.setAlignment(toggle, Qt.AlignRight)

        firstFrame.setLayout(layout)
        firstFrame.setStyleSheet(f"background-color: {'#262626' if color == 'primary' else '#343534'};")

        toggle.setChecked(plugin_name in self.activeCommands)
        toggle.stateChanged.connect(lambda: self.setActiveCommands(plugin_name, toggle.isChecked()))

        return firstFrame

    def eventFilter(self, source, event):
        if event.type() == QEvent.Enter and isinstance(source, QLabel):
            tooltip_position = source.mapToGlobal(QPoint(
                source.width() - 350,
                source.height() // 2 if self.is_searching else -source.height() // 2

            ))
            QToolTip.showText(tooltip_position, source.toolTip(), source)
        elif event.type() == QEvent.Leave and isinstance(source, QLabel):
            QToolTip.hideText()
        return super().eventFilter(source, event)

    def setActiveCommands(self, plugin_name, isChecked):
        if isChecked:
            self.activeCommands.append(plugin_name)
        else:
            self.activeCommands.remove(plugin_name)
        print(f"Plugin '{plugin_name}' toggled to {'ON' if isChecked else 'OFF'}")
        print(f"Active Commands: {self.activeCommands}")
        self.activeCommandsUpdated.emit(self.activeCommands)
        self.plugins_updated.emit(self.activeCommands)
        self.session_manager.set_activated_plugins(self.activeCommands)

    def populate_plugin_toggles(self):
        search_text = self.search_bar.text().lower()
        self.is_searching = bool(search_text)

        for i in reversed(range(self.scroll_layout.count())):
            widget = self.scroll_layout.itemAt(i).widget()
            if isinstance(widget, QFrame):
                widget.setParent(None)

        visible_plugins = [plugin for plugin in self.plugins if search_text in plugin.name.lower()]

        for i, plugin in enumerate(visible_plugins):
            color = "secondary" if (i % 2 == 0) else "primary"
            frame = self.create_plugin_toggle(plugin.name, plugin.description, color)
            self.scroll_layout.addWidget(frame)

    def change_plugin_os(self, os):
        self.os = os
        self.plugins = self.plugins_data.get_plugins(self.os)
        self.populate_plugin_toggles()
