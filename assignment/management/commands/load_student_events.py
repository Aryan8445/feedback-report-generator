import json
from django.core.management.base import BaseCommand
from assignment.tasks import generate_html_report, generate_pdf_report
import os

class Command(BaseCommand):
    help = 'Load student events from dump.json and enqueue report tasks'

    def handle(self, *args, **kwargs):
        with open(os.path.join(os.getcwd(), 'dump.json'), 'r') as f:
            data = json.load(f)
        
        for student in data:
            # You could choose to generate only HTML or PDF, or both:
            # html_task = generate_html_report.delay([student])
            pdf_task = generate_pdf_report.delay([student])
            self.stdout.write(f"Enqueued tasks for student {student['student_id']}")
            # self.stdout.write(f" - HTML task ID: {html_task.id}")
            self.stdout.write(f" - PDF task ID: {pdf_task.id}")
