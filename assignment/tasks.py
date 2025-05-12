from celery import shared_task
from bs4 import BeautifulSoup
from .models import HTMLReport, PDFReport
from .utils.html_generator import build_html_report
from .utils.pdf_generator import build_pdf_from_events

@shared_task(bind=True, name="generate_html_report")
def generate_html_report(self, data):
    try:
        if not data:
            raise ValueError("No data passed to task")

        html, student_id = build_html_report(data)

        HTMLReport.objects.create(
            task_id=self.request.id,
            student_id=student_id,
            html_content=html
        )

        return {"status": "success"}

    except Exception as e:
        raise self.retry(exc=e, countdown=5, max_retries=3)


@shared_task(bind=True, name="generate_pdf_report")
def generate_pdf_report(self, data):
    try:
        if not data:
            raise ValueError("No data passed to task")

        html, student_id = build_html_report(data)

        # Extract event sequence directly from HTML content

        soup = BeautifulSoup(html, "html.parser")
        event_text = soup.find("p").text.replace("Event Order: ", "")
        event_sequence = event_text.split(" -> ")

        pdf_bytes = build_pdf_from_events(student_id, event_sequence)

        PDFReport.objects.create(
            task_id=self.request.id,
            student_id=student_id,
            pdf_file=pdf_bytes
        )
        return {"status": "success"}

    except Exception as e:
        raise self.retry(exc=e, countdown=5, max_retries=3)
