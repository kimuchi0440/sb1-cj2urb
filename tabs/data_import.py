from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QFileDialog, QTextEdit, QInputDialog, QMessageBox
import pandas as pd
import sqlite3
import requests
import json

class DataImportTab(QWidget):
    def __init__(self, on_data_imported_callback):
        super().__init__()
        self.layout = QVBoxLayout(self)
        self.on_data_imported_callback = on_data_imported_callback

        self.excel_button = QPushButton("Excelファイルを選択 (.xlsx)")
        self.excel_button.clicked.connect(self.import_excel)
        self.layout.addWidget(self.excel_button)

        self.csv_button = QPushButton("CSVファイルを選択 (.csv)")
        self.csv_button.clicked.connect(self.import_csv)
        self.layout.addWidget(self.csv_button)

        self.clipboard_button = QPushButton("クリップボードからデータを取り込む")
        self.clipboard_button.clicked.connect(self.import_clipboard)
        self.layout.addWidget(self.clipboard_button)

        self.sqlite_button = QPushButton("SQLiteデータベースから取り込む")
        self.sqlite_button.clicked.connect(self.import_sqlite)
        self.layout.addWidget(self.sqlite_button)

        self.api_button = QPushButton("APIからデータを取得")
        self.api_button.clicked.connect(self.import_api)
        self.layout.addWidget(self.api_button)

        self.data_preview = QTextEdit()
        self.data_preview.setReadOnly(True)
        self.layout.addWidget(self.data_preview)

    def import_excel(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Excelファイルを選択", "", "Excel Files (*.xlsx)")
        if file_name:
            try:
                df = pd.read_excel(file_name)
                self.process_data(df)
            except Exception as e:
                QMessageBox.critical(self, "エラー", f"Excelファイルの読み込み中にエラーが発生しました: {str(e)}")

    def import_csv(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "CSVファイルを選択", "", "CSV Files (*.csv)")
        if file_name:
            try:
                df = pd.read_csv(file_name)
                self.process_data(df)
            except Exception as e:
                QMessageBox.critical(self, "エラー", f"CSVファイルの読み込み中にエラーが発生しました: {str(e)}")

    def import_clipboard(self):
        try:
            df = pd.read_clipboard()
            self.process_data(df)
        except Exception as e:
            QMessageBox.critical(self, "エラー", f"クリップボードからのデータ読み込み中にエラーが発生しました: {str(e)}")

    def import_sqlite(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "SQLiteデータベースを選択", "", "SQLite Files (*.db *.sqlite)")
        if file_name:
            table_name, ok = QInputDialog.getText(self, "テーブル名", "データを取得するテーブル名を入力してください:")
            if ok and table_name:
                try:
                    conn = sqlite3.connect(file_name)
                    df = pd.read_sql_query(f"SELECT * FROM {table_name}", conn)
                    conn.close()
                    self.process_data(df)
                except Exception as e:
                    QMessageBox.critical(self, "エラー", f"SQLiteデータベースからのデータ取得中にエラーが発生しました: {str(e)}")

    def import_api(self):
        api_url, ok = QInputDialog.getText(self, "API URL", "データを取得するAPIのURLを入力してください:")
        if ok and api_url:
            try:
                response = requests.get(api_url)
                data = json.loads(response.text)
                df = pd.DataFrame(data)
                self.process_data(df)
            except Exception as e:
                QMessageBox.critical(self, "エラー", f"APIからのデータ取得中にエラーが発生しました: {str(e)}")

    def process_data(self, df):
        try:
            # データの基本情報を表示
            info = f"データ形状: {df.shape}\n\n"
            info += "列情報:\n"
            for column in df.columns:
                info += f"{column}: {df[column].dtype}\n"
            info += f"\nデータプレビュー:\n{df.head().to_string()}"
            
            self.data_preview.setText(info)
            self.on_data_imported_callback(df)
            QMessageBox.information(self, "成功", "データが正常にインポートされました。")
        except Exception as e:
            QMessageBox.critical(self, "エラー", f"データの処理中にエラーが発生しました: {str(e)}")