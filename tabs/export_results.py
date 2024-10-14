from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QFileDialog, QMessageBox
import pandas as pd
import matplotlib.pyplot as plt

class ExportResultsTab(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout(self)

        self.export_csv_button = QPushButton("結果をCSVでエクスポート")
        self.export_csv_button.clicked.connect(self.export_to_csv)
        self.layout.addWidget(self.export_csv_button)

        self.export_excel_button = QPushButton("結果をExcelでエクスポート")
        self.export_excel_button.clicked.connect(self.export_to_excel)
        self.layout.addWidget(self.export_excel_button)

        self.export_image_button = QPushButton("グラフを画像でエクスポート")
        self.export_image_button.clicked.connect(self.export_to_image)
        self.layout.addWidget(self.export_image_button)

        self.results = None
        self.graph = None

    def set_results(self, results):
        self.results = results

    def set_graph(self, graph):
        self.graph = graph

    def export_to_csv(self):
        if self.results is None:
            QMessageBox.warning(self, "警告", "エクスポートする結果がありません。")
            return

        file_name, _ = QFileDialog.getSaveFileName(self, "CSVファイルを保存", "", "CSV Files (*.csv)")
        if file_name:
            try:
                self.results.to_csv(file_name, index=False)
                QMessageBox.information(self, "成功", "結果がCSVファイルにエクスポートされました。")
            except Exception as e:
                QMessageBox.critical(self, "エラー", f"CSVファイルのエクスポート中にエラーが発生しました: {str(e)}")

    def export_to_excel(self):
        if self.results is None:
            QMessageBox.warning(self, "警告", "エクスポートする結果がありません。")
            return

        file_name, _ = QFileDialog.getSaveFileName(self, "Excelファイルを保存", "", "Excel Files (*.xlsx)")
        if file_name:
            try:
                self.results.to_excel(file_name, index=False)
                QMessageBox.information(self, "成功", "結果がExcelファイルにエクスポートされました。")
            except Exception as e:
                QMessageBox.critical(self, "エラー", f"Excelファイルのエクスポート中にエラーが発生しました: {str(e)}")

    def export_to_image(self):
        if self.graph is None:
            QMessageBox.warning(self, "警告", "エクスポートするグラフがありません。")
            return

        file_name, _ = QFileDialog.getSaveFileName(self, "画像ファイルを保存", "", "PNG Files (*.png);;JPEG Files (*.jpg)")
        if file_name:
            try:
                self.graph.savefig(file_name)
                QMessageBox.information(self, "成功", "グラフが画像ファイルにエクスポートされました。")
            except Exception as e:
                QMessageBox.critical(self, "エラー", f"画像ファイルのエクスポート中にエラーが発生しました: {str(e)}")