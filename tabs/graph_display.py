from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QComboBox
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats
import numpy as np

class GraphDisplayTab(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout(self)

        self.graph_type_combo = QComboBox()
        self.graph_type_combo.addItems([
            "棒グラフ", "箱ひげグラフ", "バイオリンプロット", "散布図",
            "ヒストグラム", "カーネル密度推定", "ヒートマップ", "ペアプロット",
            "折れ線グラフ", "面グラフ", "円グラフ", "レーダーチャート"
        ])
        self.graph_type_combo.currentIndexChanged.connect(self.update_graph)
        self.layout.addWidget(QLabel("グラフタイプ:"))
        self.layout.addWidget(self.graph_type_combo)

        self.figure = Figure(figsize=(8, 6), dpi=100)
        self.canvas = FigureCanvas(self.figure)
        self.layout.addWidget(self.canvas)

        self.data = None
        self.test_type = None

    def set_data(self, data, test_type):
        self.data = data
        self.test_type = test_type
        self.update_graph()

    def update_graph(self):
        if self.data is None:
            return

        self.figure.clear()
        ax = self.figure.add_subplot(111)

        graph_type = self.graph_type_combo.currentText()

        try:
            if graph_type == "棒グラフ":
                sns.barplot(x='group', y='value', data=self.data, ax=ax)
            elif graph_type == "箱ひげグラフ":
                sns.boxplot(x='group', y='value', data=self.data, ax=ax)
            elif graph_type == "バイオリンプロット":
                sns.violinplot(x='group', y='value', data=self.data, ax=ax)
            elif graph_type == "散布図":
                sns.scatterplot(x='x', y='y', hue='group', data=self.data, ax=ax)
            elif graph_type == "ヒストグラム":
                sns.histplot(data=self.data, x='value', hue='group', element="step", stat="density", common_norm=False, ax=ax)
            elif graph_type == "カーネル密度推定":
                sns.kdeplot(data=self.data, x='value', hue='group', shade=True, ax=ax)
            elif graph_type == "ヒートマップ":
                sns.heatmap(self.data.corr(), annot=True, cmap='coolwarm', ax=ax)
            elif graph_type == "ペアプロット":
                sns.pairplot(self.data, hue='group', height=2.5)
                plt.close()  # Close the seaborn figure
                self.canvas.draw()
                return
            elif graph_type == "折れ線グラフ":
                sns.lineplot(x='x', y='value', hue='group', data=self.data, ax=ax)
            elif graph_type == "面グラフ":
                self.data.pivot(index='x', columns='group', values='value').plot(kind='area', stacked=False, ax=ax)
            elif graph_type == "円グラフ":
                self.data.groupby('group')['value'].sum().plot(kind='pie', autopct='%1.1f%%', ax=ax)
            elif graph_type == "レーダーチャート":
                self.plot_radar_chart(ax)
            else:
                ax.text(0.5, 0.5, "選択されたグラフタイプはサポートされていません", ha='center', va='center')

            ax.set_title(f"{self.test_type} - {graph_type}")
            ax.set_xlabel("グループ")
            ax.set_ylabel("値")

            self.canvas.draw()
        except Exception as e:
            print(f"グラフの作成中にエラーが発生しました: {str(e)}")

    def plot_radar_chart(self, ax):
        # Prepare the data for radar chart
        grouped_data = self.data.groupby('group')['value'].mean().reset_index()
        values = grouped_data['value'].values
        groups = grouped_data['group'].values

        # Number of variables
        num_vars = len(values)

        # Compute angle for each variable
        angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()
        values = np.concatenate((values, [values[0]]))  # complete the loop
        angles += angles[:1]  # complete the loop

        # Plot
        ax.polar(angles, values, 'o-', linewidth=2)
        ax.fill(angles, values, alpha=0.25)
        ax.set_xticks(angles[:-1])
        ax.set_xticklabels(groups)

    def clear_graph(self):
        self.figure.clear()
        self.canvas.draw()