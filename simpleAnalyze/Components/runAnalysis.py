import os
import subprocess
from PyQt5.QtCore import pyqtSignal, QObject


class RunAnalysis(QObject):
    analysis_result = pyqtSignal(list)
    progress_updated = pyqtSignal(int)

    def __init__(self, select_dump, select_plugin):
        super().__init__()
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

    def run_analysis(self):
        if self.selected_files and self.plugin:
            try:
                total_files = len(self.selected_files)
                current_file_count = 0
                summaries = []  # List to store summaries for each file
                for file, color in zip(self.selected_files, self.file_color):
                    command = ["python", "../vol.py", "-f", file, self.plugin]
                    print(f"Running command: {' '.join(command)}")  # Debugging statement
                    output = subprocess.check_output(command).decode()

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
                self.analysis_result.emit("Error: " + e.output.decode())
        else:
            self.analysis_result.emit("Error: No plugin or memory dump selected")
