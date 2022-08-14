from django import forms
from django.forms import ModelForm

from reporting_system.models import Document


class DocumentForm(ModelForm):
    class Meta:
        model = Document

        fields = ['file_name', 'pdf']

        widgets = {
            'file_name': forms.TextInput(attrs={'class': 'form-control my-1', 'placeholder': 'Dateiname'}),
            'pdf': forms.FileInput(attrs={'class': 'form-control my-1'}),
        }
