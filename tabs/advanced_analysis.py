from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QComboBox, QLabel, QTextEdit, QScrollArea
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import mean_squared_error, r2_score, accuracy_score, classification_report
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.naive_bayes import GaussianNB
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from concurrent.futures import ThreadPoolExecutor
import logging

class AdvancedAnalysisTab(QWidget):
    def __init__(self, on_analysis_completed_callback):
        super().__init__()
        self.layout = QVBoxLayout(self)
        self.on_analysis_completed_callback = on_analysis_completed_callback
        self.data = None
        self.thread_pool = ThreadPoolExecutor(max_workers=4)  # スレッドプールの初期化

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_content = QWidget()
        scroll_layout = QVBoxLayout(scroll_content)

        self.analysis_method = QComboBox()
        self.analysis_method.addItems([
            "主成分分析 (PCA)",
            "K-means クラスタリング",
            "線形回帰",
            "ロジスティック回帰",
            "サポートベクターマシン (SVM)",
            "ランダムフォレスト",
            "ナイーブベイズ"
        ])
        scroll_layout.addWidget(QLabel("分析手法:"))
        scroll_layout.addWidget(self.analysis_method)

        self.run_button = QPushButton("分析実行")
        self.run_button.clicked.connect(self.run_analysis)
        scroll_layout.addWidget(self.run_button)

        self.result_text = QTextEdit()
        self.result_text.setReadOnly(True)
        scroll_layout.addWidget(self.result_text)

        scroll_area.setWidget(scroll_content)
        self.layout.addWidget(scroll_area)

    def set_data(self, data):
        self.data = data

    def run_analysis(self):
        if self.data is None:
            self.result_text.setText("データが読み込まれていません。")
            return

        method = self.analysis_method.currentText()
        analysis_methods = {
            "主成分分析 (PCA)": self.run_pca,
            "K-means クラスタリング": self.run_kmeans,
            "線形回帰": self.run_linear_regression,
            "ロジスティック回帰": self.run_logistic_regression,
            "サポートベクターマシン (SVM)": self.run_svm,
            "ランダムフォレスト": self.run_random_forest,
            "ナイーブベイズ": self.run_naive_bayes
        }

        if method in analysis_methods:
            # 分析をスレッドプールで実行
            future = self.thread_pool.submit(analysis_methods[method])
            future.add_done_callback(self.analysis_completed)
        else:
            self.result_text.setText("選択された分析手法は実装されていません。")

    def analysis_completed(self, future):
        try:
            result, figure = future.result()
            self.result_text.setText(result)
            self.on_analysis_completed_callback(figure)
            logging.info(f"Advanced analysis '{self.analysis_method.currentText()}' completed successfully")
        except Exception as e:
            error_msg = f"分析中にエラーが発生しました: {str(e)}"
            self.result_text.setText(error_msg)
            logging.error(f"Error in advanced analysis: {str(e)}")

    # 以下、各分析手法の実装（run_pca, run_kmeans, etc.）は変更なし
    # ただし、各メソッドの最後で (result, figure) を返すように修正する

    def run_pca(self):
        # ... (既存のコード)
        return result, plt.gcf()

    def run_kmeans(self):
        # ... (既存のコード)
        return result, plt.gcf()

    def run_linear_regression(self):
        # ... (既存のコード)
        return result, plt.gcf()

    def run_logistic_regression(self):
        # ... (既存のコード)
        return result, plt.gcf()

    def run_svm(self):
        # ... (既存のコード)
        return result, plt.gcf()

    def run_random_forest(self):
        # ... (既存のコード)
        return result, plt.gcf()

    def run_naive_bayes(self):
        # ... (既存のコード)
        return result, plt.gcf()