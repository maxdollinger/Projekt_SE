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

    title = models.CharField("Bezeichnung", max_length=255, blank=False)
    description = models.TextField("Beschreibung", blank=False)
    # created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    # assigned_to = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    # qm_manager = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    assigned_at = models.DateField(default=None, blank=True, null=True)
    edited_at = models.DateField(auto_now=True)
    file_name = models.CharField("Dateiname", max_length=255, blank=False)
    file = models.FileField("Datei", upload_to='%Y/%m/%d', blank=False)
    course = models.CharField("IU Kursbezeichnung", max_length=255, blank=False)
    report_status = models.CharField("Status der Korrekturmeldung", max_length=2, choices=ReportStatus.choices, default=ReportStatus.REPORTED, null=True)
    report_type = models.CharField("Art der Korrekturmeldung", max_length=2, choices=ReportType.choices, default=ReportType.INFO, null=True)
