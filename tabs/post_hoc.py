from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QTextEdit

class PostHocTab(QWidget):
    def __init__(self, on_post_hoc_test_callback):
        super().__init__()
        self.layout = QVBoxLayout(self)
        self.on_post_hoc_test_callback = on_post_hoc_test_callback

        self.post_hoc_tests = [
            "Tukey's HSD検定", "Dunnett検定", "Bonferroni法",
            "Holm法", "Scheffe法", "Games-Howell法"
        ]

        self.create_post_hoc_buttons()

        self.result_label = QLabel("Post Hoc検定結果:")
        self.layout.addWidget(self.result_label)

        self.result_text = QTextEdit()
        self.result_text.setReadOnly(True)
        self.layout.addWidget(self.result_text)

    def create_post_hoc_buttons(self):
        for test in self.post_hoc_tests:
            button = QPushButton(test)
            button.clicked.connect(lambda checked, t=test: self.run_post_hoc(t))
            self.layout.addWidget(button)

    def run_post_hoc(self, test):
        self.on_post_hoc_test_callback(test)

    def update_results(self, results):
        self.result_text.setText(results)

    def enable_post_hoc(self, enable):
        for button in self.findChildren(QPushButton):
            button.setEnabled(enable)

    def clear_results(self):
        self.result_text.clear()