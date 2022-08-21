from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings


class CorrectionReport(models.Model):
    class ReportType(models.TextChoices):
        MISTAKE = 1, _('Fehler')
        CORRECTION = 2, _('Verbesserung')
        MISSPELLING = 3, _('Rechtschreibfehler')

    class ReportStatus(models.TextChoices):
        REPORTED = 1, _('Erstellt')
        ASSIGNED = 2, _('Zugewiesen')
        REJECTED = 3, _('Abgelehnt')
        IN_PROCESS = 4, _('In Bearbeitung')
        WAIT_FOR_FEEDBACK = 5, _('Warten auf Rückmeldung')
        COMPLETED = 6, _('Abgeschlossen')
        CHECKED = 7, _('Geprüft')

    title = models.CharField("Bezeichnung", max_length=255, blank=False)
    description = models.TextField("Beschreibung", blank=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True)
    assigned_to = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True, related_name="assignee")
    qm_manager = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True, related_name="qm_manager")
    created_at = models.DateTimeField(auto_now_add=True)
    assigned_at = models.DateTimeField(default=None, blank=True, null=True)
    edited_at = models.DateTimeField(auto_now=True)
    file_name = models.CharField("Dateiname", max_length=255, blank=True, null=True)
    file = models.FileField("Datei", upload_to='%Y/%m/%d', blank=True, null=True)
    course = models.CharField("IU Kursbezeichnung", max_length=255, blank=False)
    report_status = models.CharField("Status der Korrekturmeldung", max_length=2, choices=ReportStatus.choices, default=ReportStatus.REPORTED, null=True)
    report_type = models.CharField("Art der Korrekturmeldung", max_length=2, choices=ReportType.choices, default=ReportType.CORRECTION, null=True)