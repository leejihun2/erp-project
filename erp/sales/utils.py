from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import os
from datetime import datetime

# 📌 1. 폰트 경로 설정 및 등록
# 서버 환경에서도 에러가 나지 않도록 예외 처리를 하나로 통합했습니다.
font_path = os.path.join(os.path.dirname(__file__), 'fonts', 'malgun.ttf')

try:
    if os.path.exists(font_path):
        pdfmetrics.registerFont(TTFont('MalgunGothic', font_path))
        FONT_NAME = 'MalgunGothic'
    else:
        # 폰트 파일이 없을 경우 대비 (서버 로그에서 확인 가능)
        print(f"Warning: Font file not found at {font_path}. Falling back to Helvetica.")
        FONT_NAME = 'Helvetica'
except Exception as e:
    print(f"Font registration failed: {e}")
    FONT_NAME = 'Helvetica'

# ❌ (기존에 있던 에러 원인) 이 아래에 있던 중복된 registerFont 줄을 삭제했습니다.

def generate_estimate_pdf(response, estimate):
    doc = SimpleDocTemplate(response, pagesize=A4)
    elements = []
    styles = getSampleStyleSheet()

    # 📌 2. 결정된 FONT_NAME 적용
    # 폰트가 있으면 MalgunGothic, 없으면 Helvetica가 적용됩니다.
    styles['Normal'].fontName = FONT_NAME
    styles['Title'].fontName = FONT_NAME

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
        # 테이블 안의 폰트도 유동적으로 적용
        ('FONTNAME', (0,0), (-1,-1), FONT_NAME),

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