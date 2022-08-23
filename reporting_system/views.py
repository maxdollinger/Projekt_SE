from django.shortcuts import render, redirect
from reporting_system.forms.correction_report_form import CorrectionReportForm
from .models import CorrectionReport
from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth import get_user


def add_correction_report(request):
    if request.method == 'POST':
        form = CorrectionReportForm(request.POST, request.FILES)
        correction_report = CorrectionReport()

        if form.is_valid():
            correction_report.title = form.cleaned_data['title']
            correction_report.description = form.cleaned_data['description']
            correction_report.created_by = request.user
            correction_report.file_name = form.cleaned_data['file_name']
            correction_report.file = request.FILES['file']
            correction_report.course = form.cleaned_data['course']
            correction_report.report_type = form.cleaned_data['report_type']
            correction_report.save()
            return render(request, 'report_add.html', {
                'page_title': 'Neue Korrekturmeldung erstellen',
                'form': CorrectionReportForm(),
                'show_message': True,
                'alert': 'success',
                'message': 'Deine Korrekturmeldung wurde erfolgreich angelegt!'
            })
        else:
            return render(request, 'report_add.html', {
                'page_title': 'Neue Korrekturmeldung erstellen',
                'form': CorrectionReportForm(),
                'show_message': True,
                'alert': 'danger',
                'message': 'Leider konnte deine Korrekturmeldung nicht erfolgreich angelegt werden'
            })
    else:
        return render(request, 'report_add.html', {
            'page_title': 'Neue Korrekturmeldung erstellen',
            'form': CorrectionReportForm(),
            'show_message': False,
        })


def reports_all_view(request):
    status_filter = request.GET.get('status_filter', 'open')

    ctx = {
        'reports': get_reports_role_based(request.user, request.role, status_filter),
    }
    return render(request, "reports.html", ctx)


def reports_detail_view(request, id):
    report = CorrectionReport.objects.get(id=id)

    ctx = {
        'report': report,
    }
    return render(request, "report_detail.html", ctx)


def get_reports_role_based(user, role, filter):
    filters = {
        'open': [1, 2, 3],
        'all': [1, 2, 3, 4, 5],
    }

    if role == 'Student':
        return CorrectionReport.objects.filter(created_by=user, report_status__in=filters[filter]).order_by(
            '-edited_at')
    if role == 'Mitarbeiter IU':
        return CorrectionReport.objects.filter(assigned_to=user, report_status__in=filters[filter]).order_by(
            '-edited_at')
    if role == 'Leiter QM' or role == 'Mitarbeiter QM':
        return CorrectionReport.objects.filter(report_status__in=filters[filter]).order_by('-created_at')


def edit_correction_report(request, id):
    if request.method == "POST":
        form = CorrectionReportForm(request.POST, request.FILES)
        if 'file' in request.FILES:
            file = request.FILES['file']
        else:
            file = CorrectionReport.objects.get(id=id).file

        if form.is_valid():
            CorrectionReport.objects.filter(id=id).update(
                title=form.cleaned_data['title'],
                description=form.cleaned_data['description'],
                course=form.cleaned_data['course'],
                report_type=form.cleaned_data['report_type'],
                file_name=form.cleaned_data['file_name'],
                file=file,
                is_edited=True
            )
            return redirect(reports_detail_view, id=id)
        else:
            return render(request, 'report_edit.html', {
                'page_title': 'Korrekturmeldung bearbeiten',
                'form': CorrectionReportForm(),
                'show_message': True,
                'alert': 'danger',
                'message': 'Leider konnte deine Korrekturmeldung nicht erfolgreich bearbeitet werden!'
                           'Versuche es bitte erneut.'
            })
    else:
        report = CorrectionReport.objects.get(id=id)

        return render(request, 'report_edit.html', {
            'page_title': 'Korrekturmeldung bearbeiten',
            'form': CorrectionReportForm(instance=report),
            'report': report,
            'show_message': False,
        })
