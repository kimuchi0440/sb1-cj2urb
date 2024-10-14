from PySide6.QtWidgets import QWidget, QVBoxLayout, QTextBrowser

class HelpTab(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout(self)

        self.help_text = QTextBrowser()
        self.help_text.setOpenExternalLinks(True)
        self.layout.addWidget(self.help_text)

        self.set_help_content()

    def set_help_content(self):
        help_content = """
        <h2>統計ソフトウェアの使い方</h2>
        <ol>
            <li><strong>データ取込</strong>: ExcelファイルまたはCSVファイルからデータをインポートします。</li>
            <li><strong>データ前処理</strong>: 外れ値の処理や正規化を行います。</li>
            <li><strong>検定選択</strong>: 適切な統計検定を選択します。</li>
            <li><strong>グラフ選択</strong>: データの可視化方法を選択します。</li>
            <li><strong>統計結果</strong>: 選択した検定の結果を表示します。</li>
            <li><strong>Post Hoc</strong>: 必要に応じて、事後検定を実行します。</li>
            <li><strong>グラフ表示</strong>: 選択したグラフでデータを可視化します。</li>
            <li><strong>結果のエクスポート</strong>: 結果をCSV、Excel、または画像形式でエクスポートします。</li>
        </ol>

        <h3>統計検定の選び方</h3>
        <ul>
            <li>2群の比較: t検定またはMann-Whitney U検定</li>
            <li>3群以上の比較: 分散分析またはKruskal-Wallis検定</li>
            <li>繰り返し測定: 反復測定分散分析またはFriedman検定</li>
            <li>相関分析: Pearson相関係数またはSpearman順位相関係数</li>
        </ul>

        <p>詳細な情報は<a href="https://www.statisticshowto.com/probability-and-statistics/statistics-definitions/">Statistics How To</a>を参照してください。</p>
        """
        self.help_text.setHtml(help_content)