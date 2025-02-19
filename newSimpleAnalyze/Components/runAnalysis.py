import os
import subprocess
import sys
import logging

from PyQt5.QtCore import pyqtSignal, QObject
from PyQt5.QtWidgets import QMessageBox


logging.basicConfig(level=logging.DEBUG, filename='app.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s')

class RunAnalysis(QObject):
    analysis_result = pyqtSignal(list)
    progress_updated = pyqtSignal(int)

    def __init__(self, select_dump, select_plugin):
        super().__init__()

        try:
            self.base_path = sys._MEIPASS
        except Exception:
            self.base_path = os.path.abspath(".")

        self.plugin = []
        self.selected_files = []
        self.file_color = []
        self.select_dump = select_dump
        self.select_plugin = select_plugin
        self.select_plugin.plugin_selected.connect(self.handle_selected_plugin)

    def handle_selected_plugin(self, selected_plugin):
        self.plugin = selected_plugin

    def handle_selected_files(self, selected_files):
        self.selected_files = [file[0] for file in selected_files]
        self.file_color = [file[1] for file in selected_files]
        print("Selected color: ", self.file_color)
        print("Selected files: ", self.selected_files)

    # def get_vol_path(self):
    #     if hasattr(sys, '_MEIPASS'):
    #         return os.path.join(sys._MEIPASS, 'volatility3', 'vol.py')
    #     else:
    #         return os.path.abspath(".")

    def show_error_message(self, message):
        error_box = QMessageBox()
        error_box.setIcon(QMessageBox.Critical)
        error_box.setWindowTitle("Error")
        error_box.setText(message)
        error_box.setStandardButtons(QMessageBox.Ok)
        error_box.exec_()

    def find_vol_py(self):
        common_dirs = [
            ".",
            "..",
            "../..",
            "/usr/local/bin",
            "/usr/bin",
            "/bin",
            "/opt",
            "/usr/local/sbin",
            "/usr/sbin",
            "/sbin",
        ]

        for directory in common_dirs:
            vol_path = os.path.join(directory, "vol.py")
            if os.path.isfile(vol_path):
                return vol_path

        for root, dirs, files in os.walk("/"):
            if "vol.py" in files:
                return os.path.join(root, "vol.py")

        return None

    def run_analysis(self):
        vol_path = self.find_vol_py()
        print(vol_path)

        if not vol_path:
            self.show_error_message("Error: vol.py not found")
            return

        if self.selected_files and self.plugin:
            try:
                total_files = len(self.selected_files)
                current_file_count = 0
                summaries = []  # List to store summaries for each file
                # vol_path = self.get_vol_path()
                for file, color in zip(self.selected_files, self.file_color):
                    command = ["python", vol_path, "-f", file, self.plugin]
                    logging.debug(f"Running command: {' '.join(command)}")
                    print(f"Running command: {' '.join(command)}")  # Debugging statement
                    output = subprocess.check_output(command).decode()
                    logging.debug(f"Command output: {output}")

                    lines = output.splitlines()

                    if current_file_count == 0:
                        summary = "\n".join(lines)
                    else:
                        data_lines = lines[3:]
                        summary += "\n" + "\n".join(data_lines)

                    summaries.append((color, summary))  # Store color and summary for each file
                    current_file_count += 1

                    # Update progress
                    progress_percentage = int((current_file_count / total_files) * 100)
                    self.progress_updated.emit(progress_percentage)
                self.analysis_result.emit(summaries)
            except subprocess.CalledProcessError as e:
                logging.error(f"Subprocess error: {e.output.decode()}")
                self.analysis_result.emit([f"Error: {e.output.decode()}"])
            except Exception as e:
                logging.exception("An unexpected error occurred")
                self.show_error_message(f"Unexpected error: {str(e)}")
        else:
            self.show_error_message("Error: No plugin or memory dump selected")