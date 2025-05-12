from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
import io

def build_pdf_from_events(student_id, event_sequence):
    buffer = io.BytesIO()

    # Create PDF document
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=72,
        leftMargin=72,
        topMargin=72,
        bottomMargin=72
    )

    styles = getSampleStyleSheet()
    elements = []

    # Add title
    title = f"<b>Student ID:</b> {student_id}"
    elements.append(Paragraph(title, styles["Title"]))
    elements.append(Spacer(1, 12))

    # Wrap event sequence in paragraph
    event_text = "Event Order: " + " -> ".join(event_sequence)
    elements.append(Paragraph(event_text, styles["Normal"]))

    doc.build(elements)
    buffer.seek(0)
    return buffer.getvalue()
