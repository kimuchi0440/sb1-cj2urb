from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QComboBox, QLabel, QLineEdit, QHBoxLayout, QCheckBox, QMessageBox, QScrollArea
import pandas as pd
import numpy as np
from scipy import stats

class DataPreprocessingTab(QWidget):
    def __init__(self, on_data_preprocessed_callback):
        super().__init__()
        self.layout = QVBoxLayout(self)
        self.on_data_preprocessed_callback = on_data_preprocessed_callback
        self.data = None

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_content = QWidget()
        scroll_layout = QVBoxLayout(scroll_content)

        # 外れ値処理
        self.outlier_method = QComboBox()
        self.outlier_method.addItems(["なし", "Z-score", "IQR"])
        scroll_layout.addWidget(QLabel("外れ値処理方法:"))
        scroll_layout.addWidget(self.outlier_method)

        self.outlier_threshold = QLineEdit()
        self.outlier_threshold.setPlaceholderText("閾値（例: 3.0）")
        scroll_layout.addWidget(QLabel("外れ値閾値:"))
        scroll_layout.addWidget(self.outlier_threshold)

        # 正規化
        self.normalization_method = QComboBox()
        self.normalization_method.addItems(["なし", "標準化", "最小最大スケーリング"])
        scroll_layout.addWidget(QLabel("正規化方法:"))
        scroll_layout.addWidget(self.normalization_method)

        # 欠損値処理
        self.missing_value_method = QComboBox()
        self.missing_value_method.addItems(["なし", "削除", "平均値で補完", "中央値で補完"])
        scroll_layout.addWidget(QLabel("欠損値処理方法:"))
        scroll_layout.addWidget(self.missing_value_method)

        # カテゴリカルデータのエンコーディング
        self.encoding_method = QComboBox()
        self.encoding_method.addItems(["なし", "One-hot encoding", "Label encoding"])
        scroll_layout.addWidget(QLabel("カテゴリカルデータのエンコーディング:"))
        scroll_layout.addWidget(self.encoding_method)

        # データ変換
        self.transformation_method = QComboBox()
        self.transformation_method.addItems(["なし", "対数変換", "平方根変換"])
        scroll_layout.addWidget(QLabel("データ変換:"))
        scroll_layout.addWidget(self.transformation_method)

        self.process_button = QPushButton("データ前処理実行")
        self.process_button.clicked.connect(self.preprocess_data)
        scroll_layout.addWidget(self.process_button)

        scroll_area.setWidget(scroll_content)
        self.layout.addWidget(scroll_area)

        # データプレビュー
        self.data_preview = QTextEdit()
        self.data_preview.setReadOnly(True)
        self.layout.addWidget(QLabel("データプレビュー:"))
        self.layout.addWidget(self.data_preview)

    def set_data(self, data):
        self.data = data
        self.update_data_preview()

    def update_data_preview(self):
        if self.data is not None:
            preview = f"データ形状: {self.data.shape}\n\n"
            preview += "列情報:\n"
            for column in self.data.columns:
                preview += f"{column}: {self.data[column].dtype}\n"
            preview += f"\nデータプレビュー:\n{self.data.head().to_string()}"
            self.data_preview.setText(preview)
        else:
            self.data_preview.setText("データがありません")

    def preprocess_data(self):
        if self.data is None:
            QMessageBox.warning(self, "警告", "データが読み込まれていません。")
            return

        try:
            # 外れ値処理
            outlier_method = self.outlier_method.currentText()
            if outlier_method != "なし":
                outlier_threshold = float(self.outlier_threshold.text() or 3.0)
                if outlier_method == "Z-score":
                    z_scores = np.abs(stats.zscore(self.data.select_dtypes(include=[np.number])))
                    self.data = self.data[(z_scores < outlier_threshold).all(axis=1)]
                elif outlier_method == "IQR":
                    Q1 = self.data.select_dtypes(include=[np.number]).quantile(0.25)
                    Q3 = self.data.select_dtypes(include=[np.number]).quantile(0.75)
                    IQR = Q3 - Q1
                    self.data = self.data[~((self.data.select_dtypes(include=[np.number]) < (Q1 - outlier_threshold * IQR)) | 
                                            (self.data.select_dtypes(include=[np.number]) > (Q3 + outlier_threshold * IQR))).any(axis=1)]

            # 正規化
            normalization_method = self.normalization_method.currentText()
            if normalization_method == "標準化":
                self.data.select_dtypes(include=[np.number]) = (self.data.select_dtypes(include=[np.number]) - self.data.select_dtypes(include=[np.number]).mean()) / self.data.select_dtypes(include=[np.number]).std()
            elif normalization_method == "最小最大スケーリング":
                self.data.select_dtypes(include=[np.number]) = (self.data.select_dtypes(include=[np.number]) - self.data.select_dtypes(include=[np.number]).min()) / (self.data.select_dtypes(include=[np.number]).max() - self.data.select_dtypes(include=[np.number]).min())

            # 欠損値処理
            missing_value_method = self.missing_value_method.currentText()
            if missing_value_method == "削除":
                self.data = self.data.dropna()
            elif missing_value_method == "平均値で補完":
                self.data = self.data.fillna(self.data.mean())
            elif missing_value_method == "中央値で補完":
                self.data = self.data.fillna(self.data.median())

            # カテゴリカルデータのエンコーディング
            encoding_method = self.encoding_method.currentText()
            if encoding_method == "One-hot encoding":
                self.data = pd.get_dummies(self.data, columns=self.data.select_dtypes(include=['object', 'category']).columns)
            elif encoding_method == "Label encoding":
                for column in self.data.select_dtypes(include=['object', 'category']).columns:
                    self.data[column] = self.data[column].astype('category').cat.codes

            # データ変換
            transformation_method = self.transformation_method.currentText()
            if transformation_method == "対数変換":
                self.data.select_dtypes(include=[np.number]) = np.log1p(self.data.select_dtypes(include=[np.number]))
            elif transformation_method == "平方根変換":
                self.data.select_dtypes(include=[np.number]) = np.sqrt(self.data.select_dtypes(include=[np.number]))

            self.update_data_preview()
            self.on_data_preprocessed_callback(self.data)
            QMessageBox.information(self, "成功", "データの前処理が完了しました。")
        except Exception as e:
            QMessageBox.critical(self, "エラー", f"データの前処理中にエラーが発生しました: {str(e)}")