from datetime import datetime

from django.db import models
from django.utils.translation import gettext_lazy as _


def report_creation_date():
    return datetime.now().strftime("%Y-%m-%d")


class CorrectionReport(models.Model):
    class ReportType(models.TextChoices):
        INFO = 1, _('Hinweis')
        WARN = 2, _('Warnung')
        ERROR = 3, _('Error')
        FATAL = 4, _('Fatal')

    class ReportStatus(models.TextChoices):
        REPORTED = 1, _('Gemeldet')
        ASSIGNED = 2, _('Zugewiesen')
        IN_PROCESS = 3, _('In Bearbeitung')
        PROCESSED = 4, _('Bearbeitet')
        REJECTED = 5, _('Abgewiesen')

    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    description = models.TextField()
    # created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    # assigned_to = models.ForeignKey(User, on_delete=models.CASCADE)
    # qm_manager = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateField(default=report_creation_date())
    assigned_at = models.DateField(default=None)
    edited_at = models.DateField(default=None)
    document_name = models.CharField(max_length=255)
    course = models.CharField(max_length=255)
    report_status = models.CharField(max_length=2, choices=ReportStatus.choices, default=ReportStatus.REPORTED)
    report_type = models.CharField(max_length=2, choices=ReportType.choices, default=ReportType.INFO)
