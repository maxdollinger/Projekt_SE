from django.shortcuts import render, redirect
from reporting_system.forms.correction_report_form import CorrectionReportForm
from reporting_system.forms.document_form import DocumentForm
from reporting_system.models.correction_report import CorrectionReport
from django.shortcuts import render
from django.contrib.auth.decorators import login_required


def index(request):
    return render(request, 'cms/index.html')


def add_correction_report(request):
    if request.method == 'POST':
        form = CorrectionReportForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            return render(request, 'forms/add_correction_report.html', {
                'page_title': 'Neue Korrekturmeldung',
                'header': 'Eine neue Korrekturmeldung erstellen',
                'form': CorrectionReportForm(),
                'show_message': True,
                'alert': 'success',
                'message': 'Deine Korrekturmeldung wurde erfolgreich angelegt!'
            })
        else:
            return render(request, 'forms/add_correction_report.html', {
                'page_title': 'Neue Korrekturmeldung',
                'header': 'Eine neue Korrekturmeldung erstellen',
                'form': CorrectionReportForm(),
                'show_message': True,
                'alert': 'danger',
                'message': 'Leider konnte deine Korrekturmeldung nicht erfolgreich angelegt werden'
            })
    else:
        return render(request, 'forms/add_correction_report.html', {
            'page_title': 'Neue Korrekturmeldung',
            'header': 'Eine neue Korrekturmeldung erstellen',
            'form': CorrectionReportForm(),
            'show_message': False,
        })

def team(request):
    return render(request, 'cms/team.html')

@login_required
def overview(request):
    return render(request, "overview.html")