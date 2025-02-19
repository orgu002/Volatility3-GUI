import csv
import os
import xml.etree.ElementTree as ET
from PyQt5.QtCore import QSizeF
from PyQt5.QtGui import QTextDocument
from PyQt5.QtPrintSupport import QPrinter
from PyQt5.QtWidgets import QFileDialog, QMessageBox


class ExportManager:
    @staticmethod
    def export_data_as_xml(data, file_name):
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

        tree.write(file_name, encoding='utf-8', xml_declaration=True)

    @staticmethod
    def export_data_as_pdf(data, file_name):
        printer = QPrinter(QPrinter.HighResolution)
        printer.setOutputFormat(QPrinter.PdfFormat)
        printer.setOutputFileName(file_name)
        printer.setPaperSize(QPrinter.A4)

        html = """<html>
           <head>
           <style>
           table, th, td {
             border: 1px solid black;
             border-collapse: collapse;
             padding: 5px;
             height: auto;
           }
           </style>
           </head>"""
        html += "<table>"
        html += "<thead><tr>"
        for header in data[0].keys():
            html += "<th>{}</th>".format(header)
        html += "</tr></thead>"
        html += "<tbody>"
        for row in data:
            html += "<tr>"
            for value in row.values():
                html += "<td>{}</td>".format(value)
            html += "</tr>"
        html += "</tbody></table>"
        html += "</html>"

        doc = QTextDocument()
        doc.setHtml(html)

        try:
            doc.print_(printer)
        except Exception as e:
            QMessageBox.warning(None, "Error", f"Failed to create PDF file: {str(e)}")
            return

        QMessageBox.information(None, "Success", "PDF file exported successfully.")

    @staticmethod
    def export_data_as_csv(data, file_name):
        try:
            with open(file_name, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=data[0].keys())
                writer.writeheader()
                for row in data:
                    writer.writerow(row)
            QMessageBox.information(None, "Success", "CSV file exported successfully.")
        except Exception as e:
            QMessageBox.warning(None, "Error", f"Failed to create CSV file: {str(e)}")

    @staticmethod
    def export_data(data, parent):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getSaveFileName(parent, "Save Data As", "",
                                                   "XML Files (*.xml);;PDF Files (*.pdf);;CSV Files (*.csv);;All Files (*)",
                                                   options=options)
        if file_name:
            if file_name.endswith('.xml'):
                ExportManager.export_data_as_xml(data, file_name)
            elif file_name.endswith('.pdf'):
                ExportManager.export_data_as_pdf(data, file_name)
            elif file_name.endswith('.csv'):
                ExportManager.export_data_as_csv(data, file_name)
