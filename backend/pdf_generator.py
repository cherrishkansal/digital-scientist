from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer
)
from reportlab.lib.styles import getSampleStyleSheet


def create_pdf_report(report_text, output_file):

    doc = SimpleDocTemplate(output_file)

    styles = getSampleStyleSheet()

    content = []

    content.append(
        Paragraph("Digital Scientist Report", styles["Title"])
    )

    content.append(Spacer(1, 12))

    for line in report_text.split("\n"):
        if line.strip():
            content.append(
                Paragraph(line, styles["BodyText"])
            )

    doc.build(content)

    return output_file