import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QTabWidget, QWidget, QVBoxLayout, QToolTip, QMessageBox, QMenu, QMenuBar
from PySide6.QtGui import QFont, QAction
from tabs.test_selection import TestSelectionTab
from tabs.data_import import DataImportTab
from tabs.data_preprocessing import DataPreprocessingTab
from tabs.graph_selection import GraphSelectionTab
from tabs.statistical_results import StatisticalResultsTab
from tabs.post_hoc import PostHocTab
from tabs.graph_display import GraphDisplayTab
from tabs.export_results import ExportResultsTab
from tabs.help import HelpTab
from tabs.advanced_analysis import AdvancedAnalysisTab
from tabs.report_generation import ReportGenerationTab
from statistical_tests import run_statistical_test, run_post_hoc_test
from user_settings import UserSettings
import pandas as pd

class StatisticalSoftware(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("統計ソフトウェア")
        self.setGeometry(100, 100, 1200, 800)

        self.user_settings = UserSettings()

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        self.tabs = QTabWidget()
        self.layout.addWidget(self.tabs)

        self.data = None
        self.selected_test = None
        self.results = None

        self.test_selection_tab = TestSelectionTab(self.on_test_selected)
        self.data_import_tab = DataImportTab(self.on_data_imported)
        self.data_preprocessing_tab = DataPreprocessingTab(self.on_data_preprocessed)
        self.graph_selection_tab = GraphSelectionTab()
        self.statistical_results_tab = StatisticalResultsTab()
        self.post_hoc_tab = PostHocTab(self.on_post_hoc_test)
        self.graph_display_tab = GraphDisplayTab()
        self.export_results_tab = ExportResultsTab()
        self.help_tab = HelpTab()
        self.advanced_analysis_tab = AdvancedAnalysisTab(self.on_advanced_analysis_completed)
        self.report_generation_tab = ReportGenerationTab()

        self.tabs.addTab(self.test_selection_tab, "検定選択")
        self.tabs.addTab(self.data_import_tab, "データ取込")
        self.tabs.addTab(self.data_preprocessing_tab, "データ前処理")
        self.tabs.addTab(self.graph_selection_tab, "グラフ選択")
        self.tabs.addTab(self.statistical_results_tab, "統計結果")
        self.tabs.addTab(self.post_hoc_tab, "Post Hoc")
        self.tabs.addTab(self.graph_display_tab, "グラフ表示")
        self.tabs.addTab(self.advanced_analysis_tab, "高度な分析")
        self.tabs.addTab(self.export_results_tab, "結果のエクスポート")
        self.tabs.addTab(self.report_generation_tab, "レポート生成")
        self.tabs.addTab(self.help_tab, "ヘルプ")

        self.setup_tooltips()
        self.create_menu()
        self.load_user_settings()

    def setup_tooltips(self):
        QToolTip.setFont(QFont('SansSerif', 10))
        self.tabs.setTabToolTip(0, "適切な統計検定を選択します")
        self.tabs.setTabToolTip(1, "ExcelファイルまたはCSVファイルからデータをインポートします")
        self.tabs.setTabToolTip(2, "外れ値の処理や正規化を行います")
        self.tabs.setTabToolTip(3, "データの可視化方法を選択します")
        self.tabs.setTabToolTip(4, "選択した検定の結果を表示します")
        self.tabs.setTabToolTip(5, "必要に応じて、事後検定を実行します")
        self.tabs.setTabToolTip(6, "選択したグラフでデータを可視化します")
        self.tabs.setTabToolTip(7, "高度な統計分析や機械学習アルゴリズムを実行します")
        self.tabs.setTabToolTip(8, "結果をCSV、Excel、または画像形式でエクスポートします")
        self.tabs.setTabToolTip(9, "分析結果とグラフを含むPDFレポートを生成します")
        self.tabs.setTabToolTip(10, "ソフトウェアの使い方と統計情報を表示します")

    def create_menu(self):
        menu_bar = QMenuBar(self)
        self.setMenuBar(menu_bar)

        file_menu = QMenu("ファイル", self)
        menu_bar.addMenu(file_menu)

        save_settings_action = QAction("設定を保存", self)
        save_settings_action.triggered.connect(self.save_user_settings)
        file_menu.addAction(save_settings_action)

        load_settings_action = QAction("設定を読み込む", self)
        load_settings_action.triggered.connect(self.load_user_settings)
        file_menu.addAction(load_settings_action)

        clear_settings_action = QAction("設定をクリア", self)
        clear_settings_action.triggered.connect(self.clear_user_settings)
        file_menu.addAction(clear_settings_action)

    def save_user_settings(self):
        self.user_settings.set_setting("selected_test", self.selected_test)
        self.user_settings.set_setting("graph_type", self.graph_selection_tab.get_selected_graph_type())
        self.user_settings.set_setting("graph_customization", self.graph_selection_tab.get_customization())
        QMessageBox.information(self, "設定保存", "ユーザー設定が保存されました。")

    def load_user_settings(self):
        self.selected_test = self.user_settings.get_setting("selected_test")
        if self.selected_test:
            self.test_selection_tab.set_selected_test(self.selected_test)

        graph_type = self.user_settings.get_setting("graph_type")
        if graph_type:
            self.graph_selection_tab.set_selected_graph_type(graph_type)

        graph_customization = self.user_settings.get_setting("graph_customization")
        if graph_customization:
            self.graph_selection_tab.set_customization(graph_customization)

        QMessageBox.information(self, "設定読み込み", "ユーザー設定が読み込まれました。")

    def clear_user_settings(self):
        self.user_settings.clear_settings()
        QMessageBox.information(self, "設定クリア", "ユーザー設定がクリアされました。")

    def on_test_selected(self, test):
        self.selected_test = test
        print(f"Selected test: {test}")
        self.update_post_hoc_availability()
        if self.data is not None:
            self.run_statistical_test()

    def on_data_imported(self, data):
        self.data = data
        self.data_preprocessing_tab.set_data(data)
        self.advanced_analysis_tab.set_data(data)
        print("Data imported")
        self.update_post_hoc_availability()
        if self.selected_test is not None:
            self.run_statistical_test()

    def on_data_preprocessed(self, data):
        self.data = data
        self.advanced_analysis_tab.set_data(data)
        print("Data preprocessed")
        if self.selected_test is not None:
            self.run_statistical_test()

    def update_post_hoc_availability(self):
        if self.data is not None and self.selected_test in ["一元配置分散分析（ANOVA）", "Kruskal-Wallis検定"]:
            self.post_hoc_tab.enable_post_hoc(True)
        else:
            self.post_hoc_tab.enable_post_hoc(False)

    def run_statistical_test(self):
        try:
            results, is_significant = run_statistical_test(self.selected_test, self.data)
            self.statistical_results_tab.update_results(results, is_significant)
            self.results = pd.DataFrame({'結果': [results]})
            self.export_results_tab.set_results(self.results)
            self.report_generation_tab.set_results(self.results)
            
            graph = self.graph_display_tab.plot_graph(
                self.data,
                self.selected_test,
                self.graph_selection_tab.get_selected_graph_type(),
                self.graph_selection_tab.get_customization()
            )
            self.export_results_tab.set_graph(graph)
            self.report_generation_tab.set_graph(graph)
        except Exception as e:
            QMessageBox.critical(self, "エラー", f"統計検定の実行中にエラーが発生しました: {str(e)}")

    def on_post_hoc_test(self, test):
        try:
            results = run_post_hoc_test(test, self.data)
            self.post_hoc_tab.update_results(results)
            self.results = pd.DataFrame({'結果': [results]})
            self.export_results_tab.set_results(self.results)
            self.report_generation_tab.set_results(self.results)
        except Exception as e:
            QMessageBox.critical(self, "エラー", f"Post Hoc検定の実行中にエラーが発生しました: {str(e)}")

    def on_advanced_analysis_completed(self, results):
        self.results = results
        self.export_results_tab.set_results(self.results)
        self.report_generation_tab.set_results(self.results)
        graph = self.graph_display_tab.plot_graph(
            self.results,
            "高度な分析",
            self.graph_selection_tab.get_selected_graph_type(),
            self.graph_selection_tab.get_customization()
        )
        self.export_results_tab.set_graph(graph)
        self.report_generation_tab.set_graph(graph)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = StatisticalSoftware()
    window.show()
    sys.exit(app.exec())