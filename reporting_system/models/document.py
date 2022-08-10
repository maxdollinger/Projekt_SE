from django.db import models
from .correction_report import CorrectionReport


class Document(models.Model):
    id = models.AutoField(primary_key=True)
    correction_report = models.ForeignKey(CorrectionReport, on_delete=models.CASCADE)
    file_name = models.CharField(max_length=255)
    pdf = models.FileField(upload_to='pdf')


