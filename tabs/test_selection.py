from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QGroupBox, QPushButton, QScrollArea
from PySide6.QtCore import Qt

class TestSelectionTab(QWidget):
    def __init__(self, on_test_selected_callback):
        super().__init__()
        self.layout = QVBoxLayout(self)
        self.on_test_selected_callback = on_test_selected_callback

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        content = QWidget()
        scroll_layout = QVBoxLayout(content)

        parametric_group = self.create_test_group("パラメトリック検定", [
            "対応のないt検定", "対応のあるt検定", "一元配置分散分析（ANOVA）",
            "二元配置分散分析", "反復測定分散分析", "共分散分析（ANCOVA）"
        ])
        scroll_layout.addWidget(parametric_group)

        nonparametric_group = self.create_test_group("ノンパラメトリック検定", [
            "Mann-Whitney U検定", "Wilcoxon符号順位検定", "Kruskal-Wallis検定",
            "Friedman検定", "Spearman順位相関係数"
        ])
        scroll_layout.addWidget(nonparametric_group)

        scroll.setWidget(content)
        self.layout.addWidget(scroll)

    def create_test_group(self, title, tests):
        group = QGroupBox(title)
        group_layout = QVBoxLayout()

        for test in tests:
            button = QPushButton(test)
            button.clicked.connect(lambda checked, t=test: self.on_test_selected(t))
            group_layout.addWidget(button)

        group.setLayout(group_layout)
        return group

    def on_test_selected(self, test):
        self.on_test_selected_callback(test)