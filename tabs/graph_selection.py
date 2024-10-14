from PySide6.QtWidgets import QWidget, QVBoxLayout, QCheckBox, QGroupBox, QColorDialog, QLineEdit, QLabel, QHBoxLayout
from PySide6.QtGui import QFont

class GraphSelectionTab(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout(self)

        self.graph_types = [
            "棒グラフ", "箱ひげグラフ", "バイオリンプロット", "ドットプロット",
            "ヒストグラム", "散布図", "折れ線グラフ", "QQプロット"
        ]

        self.create_graph_selection()
        self.create_graph_customization()

    def create_graph_selection(self):
        group = QGroupBox("グラフの選択")
        group_layout = QVBoxLayout()

        for graph_type in self.graph_types:
            checkbox = QCheckBox(graph_type)
            checkbox.stateChanged.connect(self.on_graph_selected)
            group_layout.addWidget(checkbox)

        group.setLayout(group_layout)
        self.layout.addWidget(group)

    def create_graph_customization(self):
        group = QGroupBox("グラフのカスタマイズ")
        group_layout = QVBoxLayout()

        # フォント設定
        font_layout = QHBoxLayout()
        font_layout.addWidget(QLabel("フォント:"))
        self.font_input = QLineEdit()
        font_layout.addWidget(self.font_input)
        group_layout.addLayout(font_layout)

        # グラフ名
        graph_name_layout = QHBoxLayout()
        graph_name_layout.addWidget(QLabel("グラフ名:"))
        self.graph_name_input = QLineEdit()
        graph_name_layout.addWidget(self.graph_name_input)
        group_layout.addLayout(graph_name_layout)

        # X軸、Y軸の名前
        axis_name_layout = QHBoxLayout()
        axis_name_layout.addWidget(QLabel("X軸名:"))
        self.x_axis_name_input = QLineEdit()
        axis_name_layout.addWidget(self.x_axis_name_input)
        axis_name_layout.addWidget(QLabel("Y軸名:"))
        self.y_axis_name_input = QLineEdit()
        axis_name_layout.addWidget(self.y_axis_name_input)
        group_layout.addLayout(axis_name_layout)

        # X軸、Y軸の最大値および目盛間隔の設定
        axis_settings_layout = QHBoxLayout()
        axis_settings_layout.addWidget(QLabel("X軸最大値:"))
        self.x_max_input = QLineEdit()
        axis_settings_layout.addWidget(self.x_max_input)
        axis_settings_layout.addWidget(QLabel("X軸目盛間隔:"))
        self.x_tick_input = QLineEdit()
        axis_settings_layout.addWidget(self.x_tick_input)
        group_layout.addLayout(axis_settings_layout)

        y_axis_settings_layout = QHBoxLayout()
        y_axis_settings_layout.addWidget(QLabel("Y軸最大値:"))
        self.y_max_input = QLineEdit()
        y_axis_settings_layout.addWidget(self.y_max_input)
        y_axis_settings_layout.addWidget(QLabel("Y軸目盛間隔:"))
        self.y_tick_input = QLineEdit()
        y_axis_settings_layout.addWidget(self.y_tick_input)
        group_layout.addLayout(y_axis_settings_layout)

        # 色の設定
        self.color_button = QPushButton("グラフの色を設定")
        self.color_button.clicked.connect(self.select_color)
        group_layout.addWidget(self.color_button)

        group.setLayout(group_layout)
        self.layout.addWidget(group)

    def on_graph_selected(self):
        selected_graphs = [checkbox.text() for checkbox in self.findChildren(QCheckBox) if checkbox.isChecked()]
        print(f"Selected graphs: {selected_graphs}")

    def select_color(self):
        color = QColorDialog.getColor()
        if color.isValid():
            print(f"Selected color: {color.name()}")

    def get_customization(self):
        return {
            'font': self.font_input.text(),
            'graph_name': self.graph_name_input.text(),
            'x_axis_name': self.x_axis_name_input.text(),
            'y_axis_name': self.y_axis_name_input.text(),
            'x_max': self.x_max_input.text(),
            'x_tick': self.x_tick_input.text(),
            'y_max': self.y_max_input.text(),
            'y_tick': self.y_tick_input.text(),
        }

    def get_selected_graph_type(self):
        for checkbox in self.findChildren(QCheckBox):
            if checkbox.isChecked():
                return checkbox.text()
        return None