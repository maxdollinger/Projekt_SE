from django import forms
from django.forms import ModelForm

from reporting_system.models import CorrectionReport


class CorrectionReportForm(ModelForm):
    class Meta:
        model = CorrectionReport
        fields = ('title', 'description', 'file_name', 'course', 'report_type', 'file', 'created_by')

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control my-1', 'placeholder': 'Korrekturmeldung'}),
            'description': forms.Textarea(attrs={'class': 'form-control my-1', 'placeholder': 'Beschreibe deine Korrekturmeldung'}),
            'file_name': forms.TextInput(attrs={'class': 'form-control my-1', 'placeholder': 'Dateiname'}),
            'course': forms.TextInput(attrs={'class': 'form-control my-1', 'placeholder': 'IMT101'}),
            'report_type': forms.Select(attrs={'class': 'form-control my-1', 'placeholder': 'Art der Meldung'}),
            'file': forms.FileInput(attrs={'class': 'form-control my-1'}),
        }


class CorrectionReportStudentForm(ModelForm):
    class Meta:
        model = CorrectionReport
        fields = ('title', 'description', 'file_name', 'course', 'file')

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control my-1', 'placeholder': 'Korrekturmeldung'}),
            'description': forms.Textarea(attrs={'class': 'form-control my-1', 'placeholder': 'Beschreibe deine Korrekturmeldung'}),
            'file_name': forms.TextInput(attrs={'class': 'form-control my-1', 'placeholder': 'Dateiname'}),
            'course': forms.TextInput(attrs={'class': 'form-control my-1', 'placeholder': 'IMT101'}),
            'file': forms.FileInput(attrs={'class': 'form-control my-1'}),
        }

class CorrectionReportEMPForm(ModelForm):
    class Meta:
        model = CorrectionReport
        fields = ('report_status', 'comment')

        widgets = {
            'report_status': forms.Select(attrs={'class': 'form-control my-1', 'placeholder': 'Status der Meldung'}),
            'comment': forms.Textarea(attrs={'class': 'form-control my-1', 'placeholder': 'Kommentar'}),
        }

class CorrectionReportQMForm(ModelForm):
    class Meta:
        model = CorrectionReport
        fields = ('report_type', 'report_status', 'comment')

        widgets = {
            'report_type': forms.Select(attrs={'class': 'form-control my-1', 'placeholder': 'Art der Meldung'}),
            'report_status': forms.Select(attrs={'class': 'form-control my-1', 'placeholder': 'Status der Meldung'}),
            'comment': forms.Textarea(attrs={'class': 'form-control my-1', 'placeholder': 'Kommentar'}),
        }
