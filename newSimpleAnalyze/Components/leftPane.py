
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QGroupBox, QListWidget, QListWidgetItem, QLabel
from PyQt5.QtCore import Qt

class LeftPaneWidget(QWidget):
    def __init__(self):
        super().__init__()

        left_pane_layout = QVBoxLayout(self)

        dumps_group = QGroupBox("DUMPS")
        dumps_layout = QVBoxLayout()
        self.dumps_list = QListWidget()

        self.dumps_list.addItem(QListWidgetItem("Infected.vmem"))
        self.dumps_list.addItem(QListWidgetItem("windows_02"))
        self.dumps_list.addItem(QListWidgetItem("windows_03"))
        self.dumps_list.addItem(QListWidgetItem("windows_04"))
        for i in range(self.dumps_list.count()):
            item = self.dumps_list.item(i)
            item.setFlags(item.flags() | Qt.ItemIsUserCheckable)
            item.setCheckState(Qt.Unchecked)
        dumps_layout.addWidget(self.dumps_list)
        dumps_group.setLayout(dumps_layout)
        dumps_group.setFixedHeight(200)
        left_pane_layout.addWidget(dumps_group)


        plugins_group = QGroupBox("PLUGINS")
        plugins_layout = QVBoxLayout()
        self.plugins_list = QListWidget()

        plugins_subheader = QLabel("Choose plugins to analyze memory dump")
        plugins_subheader.setStyleSheet("color: #D3D3D3 ; font-size: 9px;")
        plugins_layout.addWidget(plugins_subheader)

        plugins = ["windows.pslist", "windows.dlllist", "windows.info", "windows.pstree", "windows.psscan",
                   "windows.netscan", "windows.callbacks", "windows.svcscan", "windows.registry.hivelist",
                   "windows.registry.printkey", "windows.malfind", "windows.cmdline", "windows.getservicesids",
                   "windows.modules", "windows.driverscan", "windows.verinfo", "windows.vadinfo",
                   "windows.devicetree", "windows.handles", "windows.bigpools", "windows.mbr", "windows.threads"]
        for plugin in plugins:
            item = QListWidgetItem(plugin)
            item.setFlags(item.flags() | Qt.ItemIsUserCheckable)
            item.setCheckState(Qt.Unchecked)
            self.plugins_list.addItem(item)
        plugins_layout.addWidget(self.plugins_list)

        plugins_group.setLayout(plugins_layout)
        left_pane_layout.addWidget(plugins_group)


        self.apply_styles()

    def apply_styles(self):
        self.setStyleSheet("""
                QGroupBox {
                    font: bold 14px;
                    color: #FFFFFF;
                    margin-top: 10px;
                    border-radius: 5px;
                }
                QGroupBox::title {
                    subcontrol-origin: margin;
                    subcontrol-position: top left;
                    padding: 0 3px;
                    border-bottom: 2px solid #FFA500;
                }
                QListWidget {
                    border-radius: 5px;
                    background-color: #333;
                }
                QListWidget::item {
                    color: #FFF;
                    height: 25px;
                    background-color: #333;
                }
                QListWidget::item:selected {
                    background-color: #FFFFFF;
                    color: #333;
                }
            """)
