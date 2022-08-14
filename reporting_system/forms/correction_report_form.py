from django import forms
from django.forms import ModelForm

from reporting_system.models import CorrectionReport


class CorrectionReportForm(ModelForm):
    class Meta:
        model = CorrectionReport

        fields = ['title', 'description', 'course', 'document_name', 'report_type']

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control my-1', 'placeholder': 'Korrekturmeldung'}),
            'description': forms.Textarea(attrs={'class': 'form-control my-1', 'placeholder': 'Beschreibe deine Korrekturmeldung'}),
            'course': forms.TextInput(attrs={'class': 'form-control my-1', 'placeholder': 'IMT101'}),
            'document_name': forms.TextInput(attrs={'class': 'form-control my-1'}),
            'report_type': forms.Select(attrs={'class': 'form-control my-1', 'placeholder': 'Art der Meldung'})
        }
