from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QTextEdit, QScrollArea

class StatisticalResultsTab(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout(self)

        self.result_label = QLabel("統計結果:")
        self.layout.addWidget(self.result_label)

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.layout.addWidget(self.scroll_area)

        self.result_text = QTextEdit()
        self.result_text.setReadOnly(True)
        self.scroll_area.setWidget(self.result_text)

        self.significance_label = QLabel()
        self.layout.addWidget(self.significance_label)

    def update_results(self, results, is_significant):
        self.result_text.setPlainText(results)
        if is_significant:
            self.significance_label.setText("有意差あり (p < 0.05)")
        else:
            self.significance_label.setText("有意差なし (p ≥ 0.05)")

    def clear_results(self):
        self.result_text.clear()
        self.significance_label.clear()