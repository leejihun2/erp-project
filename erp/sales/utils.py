from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import os
from datetime import datetime


# 폰트 등록
font_path = os.path.join(os.path.dirname(__file__), 'fonts', 'malgun.ttf')
pdfmetrics.registerFont(TTFont('MalgunGothic', font_path))


def generate_estimate_pdf(response, estimate):
    doc = SimpleDocTemplate(response, pagesize=A4)
    elements = []
    styles = getSampleStyleSheet()

    # 폰트 적용
    styles['Normal'].fontName = 'MalgunGothic'
    styles['Title'].fontName = 'MalgunGothic'

    # 📌 회사명
    elements.append(Paragraph("타이거몰드앤베이스", styles['Title']))
    elements.append(Spacer(1, 20))

    # 📌 문서 제목
    elements.append(Paragraph("견 적 서", styles['Title']))
    elements.append(Spacer(1, 20))

    # 📌 기본 정보
    elements.append(Paragraph(f"고객사: {estimate.client.name}", styles['Normal']))
    elements.append(Paragraph(f"견적명: {estimate.title}", styles['Normal']))
    elements.append(Paragraph(f"작성일: {datetime.now().strftime('%Y-%m-%d')}", styles['Normal']))
    elements.append(Spacer(1, 20))

    # 📌 표 데이터
    data = [['품목명', '단가', '수량', '금액']]

    total = 0
    for item in estimate.items.all():
        row_total = item.price * item.quantity
        total += row_total

        data.append([
            item.name,
            f"{item.price:,}",
            item.quantity,
            f"{row_total:,}"
        ])

    # 총합
    data.append(['', '', '총합', f"{total:,} 원"])

    # 📌 테이블 생성
    table = Table(data, colWidths=[150, 100, 80, 120])

    table.setStyle(TableStyle([
        ('FONTNAME', (0,0), (-1,-1), 'MalgunGothic'),

        # 헤더
        ('BACKGROUND', (0,0), (-1,0), colors.grey),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),

        # 정렬
        ('ALIGN', (1,1), (-1,-1), 'RIGHT'),
        ('ALIGN', (0,0), (-1,0), 'CENTER'),

        # 테두리
        ('GRID', (0,0), (-1,-1), 1, colors.black),

        # 총합 강조
        ('BACKGROUND', (0,-1), (-1,-1), colors.lightgrey),
        ('SPAN', (0,-1), (2,-1)),
        ('ALIGN', (0,-1), (2,-1), 'RIGHT'),
    ]))

    elements.append(table)

    doc.build(elements)