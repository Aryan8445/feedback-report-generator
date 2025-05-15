from django.db import models

class HTMLReport(models.Model):
    task_id = models.CharField(max_length=255)  
    student_id = models.CharField(max_length=255)
    html_content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

class PDFReport(models.Model):
    task_id = models.CharField(max_length=255)
    student_id = models.CharField(max_length=255)
    pdf_file = models.BinaryField()
    created_at = models.DateTimeField(auto_now_add=True)