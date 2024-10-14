from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QFileDialog, QMessageBox, QTextEdit, QLabel
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from io import BytesIO
import matplotlib.pyplot as plt

class ReportGenerationTab(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout(self)
        
        self.title_input = QTextEdit()
        self.title_input.setPlaceholderText("レポートのタイトルを入力してください")
        self.layout.addWidget(QLabel("レポートタイトル:"))
        self.layout.addWidget(self.title_input)

        self.description_input = QTextEdit()
        self.description_input.setPlaceholderText("レポートの説明を入力してください")
        self.layout.addWidget(QLabel("レポートの説明:"))
        self.layout.addWidget(self.description_input)

        self.generate_report_button = QPushButton("レポート生成")
        self.generate_report_button.clicked.connect(self.generate_report)
        self.layout.addWidget(self.generate_report_button)
        
        self.results = None
        self.graph = None

    def set_results(self, results):
        self.results = results

    def set_graph(self, graph):
        self.graph = graph

    def generate_report(self):
        if self.results is None:
            QMessageBox.warning(self, "警告", "レポートに含める結果がありません。")
            return

        file_name, _ = QFileDialog.getSaveFileName(self, "レポートを保存", "", "PDF Files (*.pdf)")
        if file_name:
            try:
                doc = SimpleDocTemplate(file_name, pagesize=letter)
                styles = getSampleStyleSheet()
                story = []

                # カスタムスタイルの定義
                styles.add(ParagraphStyle(name='CustomTitle', fontSize=24, alignment=1, spaceAfter=20))
                styles.add(ParagraphStyle(name='CustomHeading', fontSize=18, spaceAfter=12))
                styles.add(ParagraphStyle(name='CustomBody', fontSize=12, spaceAfter=6))

                # タイトル
                title = self.title_input.toPlainText() or "統計分析レポート"
                story.append(Paragraph(title, styles['CustomTitle']))
                story.append(Spacer(1, 20))

                # 説明
                description = self.description_input.toPlainText()
                if description:
                    story.append(Paragraph("概要:", styles['CustomHeading']))
                    story.append(Paragraph(description, styles['CustomBody']))
                    story.append(Spacer(1, 12))

                # 分析結果
                story.append(Paragraph("分析結果:", styles['CustomHeading']))
                data = [['項目', '値']]
                for index, row in self.results.iterrows():
                    for column, value in row.items():
                        data.append([column, str(value)])
                
                table = Table(data)
                table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, 0), 14),
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                    ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                    ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                    ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                    ('FONTSIZE', (0, 1), (-1, -1), 12),
                    ('BOTTOMPADDING', (0, 1), (-1, -1), 6),
                    ('GRID', (0, 0), (-1, -1), 1, colors.black)
                ]))
                story.append(table)
                story.append(Spacer(1, 12))

                # グラフ
                if self.graph:
                    story.append(Paragraph("グラフ:", styles['CustomHeading']))
                    img_data = BytesIO()
                    self.graph.savefig(img_data, format='png', dpi=300, bbox_inches='tight')
                    img_data.seek(0)
                    img = Image(img_data, width=400, height=300)
                    story.append(img)

                doc.build(story)
                QMessageBox.information(self, "成功", "レポートが生成されました。")
            except Exception as e:
                QMessageBox.critical(self, "エラー", f"レポート生成中にエラーが発生しました: {str(e)}")