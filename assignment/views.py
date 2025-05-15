from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from celery.result import AsyncResult
from .tasks import generate_html_report, generate_pdf_report
from .models import HTMLReport, PDFReport
from django.http import HttpResponse, FileResponse
import io
import zipfile

class HTMLReportView(APIView):
    def post(self, request):
        data = request.data

        # Normalize payload format
        if isinstance(data, dict):
            data = [data]
        elif isinstance(data, list) and all(isinstance(s, dict) and 'student_id' in s for s in data):
            pass
        else:
            return Response({"error": "Invalid data format."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            task = generate_html_report.delay(data)
            return Response({"task_id": task.id}, status=status.HTTP_202_ACCEPTED)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class HTMLReportStatusView(APIView):
    def get(self, request, task_id):
        task = AsyncResult(task_id)

        if task.state == "PENDING":
            return Response({"status": "pending"})
        elif task.state == "FAILURE":
            return Response({"status": "failed"})
        elif task.state == "SUCCESS":
            reports = HTMLReport.objects.filter(task_id=task_id)

            if not reports.exists():
                return Response({"status": "not found"}, status=status.HTTP_404_NOT_FOUND)

            report_data = []
            for report in reports:
                report_data.append({
                    "student_id": report.student_id,
                    "html": report.html_content
                })

            return Response({
                "status": "completed",
                "reports": report_data
            })

        return Response({"status": task.state})

class PDFReportView(APIView):
    def post(self, request):
        task = generate_pdf_report.delay(request.data)
        return Response({"task_id": task.id}, status=status.HTTP_202_ACCEPTED)

class PDFReportStatusView(APIView):
    def get(self, request, task_id):
        task = AsyncResult(task_id)

        if task.state == "PENDING":
            return Response({"status": "pending"})
        elif task.state == "FAILURE":
            return Response({"status": "failed"})
        elif task.state == "SUCCESS":
            pdf_reports = PDFReport.objects.filter(task_id=task_id)

            if not pdf_reports.exists():
                return Response({"status": "not found"}, status=status.HTTP_404_NOT_FOUND)

            if pdf_reports.count() == 1:
                report = pdf_reports.first()
                response = HttpResponse(report.pdf_file, content_type='application/pdf')
                response['Content-Disposition'] = f'attachment; filename="{report.student_id}_report.pdf"'
                return response

            # If multiple students: bundle into ZIP
            zip_buffer = io.BytesIO()
            with zipfile.ZipFile(zip_buffer, "w") as zip_file:
                for report in pdf_reports:
                    filename = f"{report.student_id}_report.pdf"
                    zip_file.writestr(filename, report.pdf_file)

            zip_buffer.seek(0)
            response = FileResponse(zip_buffer, content_type='application/zip')
            response['Content-Disposition'] = f'attachment; filename="pdf_reports_{task_id}.zip"'
            return response

        return Response({"status": task.state})