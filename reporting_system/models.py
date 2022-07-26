from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.core.validators import MinLengthValidator
import os


class CorrectionReport(models.Model):
    class DocumentType(models.TextChoices):
        SCRIPT = 1, _('Skript')
        LITERATURE = 2, _('Literaturliste')
        ONLINE_TESTS = 3, _('Online Tests')
        EVALUATION = 4, _('Kursevaluation')
        EXAM = 5, _('Musterklausur')
        EXAM_SOLUTIONS = 6, _('Musterlösung')
        SLIDE_SET = 7, _('Foliensätze für Präsenzstudium')
        PODCAST = 8, _('Podcast')
        PRESENTATION = 9, _('Präsentation')
        INTERACTIVE_LECTURE = 10, _('Interaktive Lehrveranstaltung')
        TUTORIAL = 11, _('Tutorium')
        TUTORIAL_DOCUMENTS = 12, _('Dokumente Tutorium')
        REPETITORIUM = 13, _('Repetitorium')
        LEARNING_SPRINT = 14, _('Learning Sprint')
        WORKBOOK = 15, _('Workbook Aufgaben')
        BOOTCAMP = 16, _('Bootcamp')
        SHORTCAST = 17, _('Shortcast')
        LIVE_TUTORIAL = 18, _('Live-Tutorial')
        TASK = 19, _('Aufgabenstellung: Schriftliche Ausarbeitung')
        GALLERY = 20, _('Videogalerie')
        PRE_ASSESSMENT = 21, _('Pre-Assessment')
        OTHER = 22, _('Sonstige Dokumente')

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

    title = models.CharField("Bezeichnung", max_length=254, blank=False, error_messages={
        'required': 'Bitte vergebe für deine Korrekturmeldung eine Bezeichnung.',
        'max_length': 'Die Bezeichnung darf maximal 254 Zeichen lang sein.'
    }, validators=[MinLengthValidator(10, message='Die Bezeichnung muss mindestens 10 Zeichen lang sein')])
    description = models.TextField("Beschreibung", blank=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True)
    assigned_to = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True, related_name="assignee")
    qm_manager = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True, related_name="qm_manager")
    created_at = models.DateTimeField(auto_now_add=True)
    assigned_at = models.DateTimeField(default=None, blank=True, null=True)
    edited_at = models.DateTimeField(auto_now=True)
    file_name = models.CharField("Dateiname", max_length=254, blank=True, null=True, error_messages={
        'max_length': 'Der Dateiname darf maximal 254 Zeichen lang sein.'
    }, validators=[MinLengthValidator(10, message='Der Dateiname muss mindestens 10 Zeichen lang sein.')])
    file = models.FileField("Datei", upload_to='%Y/%m/%d', blank=True, null=True)
    course = models.CharField("IU Kursbezeichnung", max_length=255, blank=False, error_messages={
        'max_length': 'Die IU Kursbezeichnung darf maximal 255 Zeichen lang sein.'
    })
    comment = models.TextField("Ablehnungs Grund", blank=True, null=True)
    report_status = models.CharField("Status der Korrekturmeldung", max_length=255, choices=ReportStatus.choices,
                                     default=ReportStatus.REPORTED, null=True, blank=True)
    report_type = models.CharField("Art der Korrekturmeldung", max_length=255, choices=ReportType.choices,
                                   default=ReportType.CORRECTION, null=True)
    document_type = models.CharField("Lehrmaterial", max_length=255, choices=DocumentType.choices,
                                     default=DocumentType.SCRIPT)

    def delete(self, *args, **kwargs):
        if self.file :
            self.file.storage.delete(self.file.name)
        super().delete()
