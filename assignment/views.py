from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from celery.result import AsyncResult
from .tasks import generate_html_report, generate_pdf_report
from .models import HTMLReport, PDFReport
from django.http import HttpResponse

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
            try:
                report = HTMLReport.objects.get(task_id=task_id)
                return Response({"status": "completed", "html": report.html_content})
            except HTMLReport.DoesNotExist:
                return Response({"status": "not found"}, status=status.HTTP_404_NOT_FOUND)
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
            try:
                report = PDFReport.objects.get(task_id=task_id)
                return HttpResponse(report.pdf_file, content_type='application/pdf')
            except PDFReport.DoesNotExist:
                return Response({"status": "not found"}, status=status.HTTP_404_NOT_FOUND)
        return Response({"status": task.state})
