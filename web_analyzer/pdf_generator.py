from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus.flowables import HRFlowable

def create_pdf(data, filename="output.pdf"):
    doc = SimpleDocTemplate(filename, pagesize=letter,
                            rightMargin=72, leftMargin=72,
                            topMargin=72, bottomMargin=72)

    styles = getSampleStyleSheet()
    story = []

    title_style = ParagraphStyle('Title', parent=styles['Heading1'], fontSize=20, textColor=colors.HexColor('#2B6CB0'))
    section_style = ParagraphStyle('Section', parent=styles['Heading2'], fontSize=14, textColor=colors.HexColor('#2C5282'))
    bullet_style = ParagraphStyle('Bullet', parent=styles['Normal'], bulletIndent=5, fontSize=10, textColor=colors.HexColor('#4A5568'))
    summary_style = ParagraphStyle('Summary', parent=styles['BodyText'], fontSize=11, textColor=colors.HexColor('#4A5568'))

    story.append(Paragraph("Website Content Analysis Report", title_style))
    story.append(Paragraph(f"<b>URL:</b> {data['url']}", styles['Normal']))
    story.append(HRFlowable(width="100%", color=colors.HexColor('#CBD5E0')))
    story.append(Spacer(1, 12))

    story.append(Paragraph("Summary", section_style))
    story.append(Paragraph(data["summary"], summary_style))

    story.append(Paragraph("Entities", section_style))
    for key in ["persons", "organizations", "locations"]:
        if data["entities"].get(key):
            story.append(Paragraph(key.capitalize(), styles["Heading3"]))
            for item in data["entities"][key]:
                story.append(Paragraph(f"• {item}", bullet_style))

    doc.build(story)