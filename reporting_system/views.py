from datetime import datetime

from django.shortcuts import render, redirect
from reporting_system.forms.correction_report_form import CorrectionReportEMPForm, CorrectionReportForm
from reporting_system.forms.correction_report_form import CorrectionReportQMForm
from reporting_system.forms.correction_report_form import CorrectionReportStudentForm
from .models import CorrectionReport
from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.contrib import messages
from .services import get_assignee_users, get_user_role, get_qm_users, Roles, roles_are_valid
from django.contrib.auth.decorators import login_required
import os
from django.core.files.storage import default_storage
from django.db.models import Q

@login_required
def add_correction_report(request):
    if request.method == 'POST':
        form = CorrectionReportForm(request.POST, request.FILES)
        correction_report = CorrectionReport()

        if 'file' in request.FILES:
            file = request.FILES['file']
            if file.size >= 10_455_040:
                messages.warning(
                    request, 'Dateien dürfen nicht größer als 10 MB sein.')
                return render(request, 'report_add.html', {
                    'page_title': 'Neue Korrekturmeldung',
                    'form': form,
                })
        else:
            file = None

        if form.is_valid():
            if 'file' in request.FILES and form.cleaned_data['file_name'] is None:
                messages.warning(request, 'Bitte lege einen Dateinamen fest, wenn du eine Datei an die '
                                          'Korrekturmeldung anhängst.')
                return render(request, 'report_add.html', {
                    'page_title': 'Neue Korrekturmeldung',
                    'form': form,
                })

            if form.cleaned_data['file_name'] is not None and 'file' not in request.FILES:
                messages.warning(
                    request, 'Bitte hänge eine Datei an, wenn du einen Dateinamen festlegst.')
                return render(request, 'report_add.html', {
                    'page_title': 'Neue Korrekturmeldung',
                    'form': form,
                })

            correction_report.title = form.cleaned_data['title']
            correction_report.description = form.cleaned_data['description']
            correction_report.created_by = request.user
            correction_report.file_name = form.cleaned_data['file_name']
            correction_report.file = file
            correction_report.course = form.cleaned_data['course']
            correction_report.document_type = form.cleaned_data['document_type']
            correction_report.report_type = form.cleaned_data['report_type']
            correction_report.save()
            messages.success(
                request, "Deine Korrekturmeldung wurde erfolgreich angelegt.")
            return redirect(reports_detail_view, id=correction_report.id)
        else:
            messages.error(
                request, 'Leider konnte deine Korrekturmeldung nicht erfolgreich angelegt werden.')
            return render(request, 'report_add.html', {
                'page_title': 'Neue Korrekturmeldung',
                'form': form,
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
        'assignees': get_assignee_users(),
        'managers': get_qm_users(),
        'creator': report.created_by,
        'role': get_user_role(request.user)
    }
    return render(request, "report_detail.html", ctx)


def get_reports_role_based(user, role, filter):
    filters = {
        'open': [1, 2, 4, 5, 7],
        'all': [1, 2, 3, 4, 5, 6, 7],
    }

    if role == 'Student':
        return CorrectionReport.objects.filter(created_by=user, report_status__in=filters[filter]).order_by(
            '-edited_at')
    if role == 'Mitarbeiter IU':
        return CorrectionReport.objects.filter(Q(assigned_to=user) | Q(created_by=user), report_status__in=filters[filter]).order_by(
            '-edited_at')
    if role == 'Leiter QM' or role == 'Mitarbeiter QM':
        return CorrectionReport.objects.filter(report_status__in=filters[filter]).order_by('-created_at')


@login_required
def edit_report_student(request, id):
    if request.method == "POST":
        report = CorrectionReport.objects.get(id=id)

        if request.user != report.created_by:
            messages.error(
                request, "Nur der Ersteller einer Korrekturmeldung darf die Daten bearbeiten.")
            return redirect(reports_all_view)

        form = CorrectionReportStudentForm(request.POST, request.FILES)

        if 'file' in request.FILES:
            file = request.FILES['file']
            file.name = file.name.replace(" ", "_")

            delete_file(report.file.path)
            default_storage.save(file.name, file)
            print(f"The file {file.name} has been saved successfully")
        else:
            if report.file is None:
                file = None
            else:
                file = report.file

        if form.is_valid():
            CorrectionReport.objects.filter(id=id).update(
                title=form.cleaned_data['title'],
                description=form.cleaned_data['description'],
                course=form.cleaned_data['course'],
                document_type=form.cleaned_data['document_type'],
                file_name=form.cleaned_data['file_name'],
                edited_at=datetime.now(),
                file=file
            )
            messages.success(
                request, "Die Änderungen deiner Korrekturmeldung wurden erfolgreich gespeichert.")
            return redirect(reports_detail_view, id=id)
        else:
            messages.error(
                request, 'Deine Änderungen an der Korrekturmeldungen konnten nicht gespeichert werden.')
            return render(request, 'report_edit_student.html', {
                'page_title': 'Korrekturmeldung bearbeiten',
                'form': form,
                'report': report,
                'role': get_user_role(request.user),
            })
    else:
        report = CorrectionReport.objects.get(id=id)

        return render(request, 'report_edit_student.html', {
            'page_title': 'Korrekturmeldung bearbeiten',
            'form': CorrectionReportStudentForm(instance=report),
            'report': report,
            'role': get_user_role(request.user),
        })


@login_required
def edit_report_emp(request, id):
    if not roles_are_valid(request, [Roles.IU_EMPLOYEE.value]):
        return redirect(reports_all_view)

    if request.method == "POST":
        form = CorrectionReportEMPForm(request.POST.copy())

        if form.data['report_status'] != "3":
            form.data['comment'] = None

        if form.is_valid():
            CorrectionReport.objects.filter(id=id).update(
                report_status=form.cleaned_data['report_status'],
                comment=form.cleaned_data['comment'],
                edited_at=datetime.now(),
            )
            messages.success(request, "Die Änderungen deiner Korrekturmeldung wurden erfolgreich gespeichert.")
            return redirect(reports_detail_view, id=id)
        else:
            messages.error(request, 'Deine Änderungen an der Korrekturmeldungen konnten nicht gespeichert werden.')
            return render(request, 'report_edit_qm.html', {
                'page_title': 'Status ändern',
                'form': form,
                'report': report,
            })
    else:
        report = CorrectionReport.objects.get(id=id)

        return render(request, 'report_edit_emp.html', {
            'page_title': 'Status ändern',
            'form': CorrectionReportEMPForm(instance=report),
            'report': report,
        })

@login_required
def edit_report_qm(request, id):
    if not roles_are_valid(request, [Roles.QM_MANAGER.value, Roles.QM_LEADER.value]):
        return redirect(reports_all_view)

    if request.method == "POST":
        form = CorrectionReportQMForm(request.POST.copy())
        report = CorrectionReport.objects.get(id=id)

        if form.data['report_status'] != "3":
            form.data['comment'] = None

        if form.is_valid():
            if 'qm_user_id' in request.POST:
                qm_manager = User.objects.get(id=request.POST['qm_user_id'])
            else:
                if report.qm_manager is not None:
                    qm_manager = report.qm_manager
                else:
                    qm_manager = None

            CorrectionReport.objects.filter(id=id).update(
                report_type=form.cleaned_data['report_type'],
                report_status=form.cleaned_data['report_status'],
                comment=form.cleaned_data['comment'],
                edited_at=datetime.now(),
                qm_manager=qm_manager
            )
            messages.success(request, "Die Änderungen deiner Korrekturmeldung wurden erfolgreich gespeichert.")
            return redirect(reports_detail_view, id=id)
        else:
            messages.error(request, 'Deine Änderungen an der Korrekturmeldungen konnten nicht gespeichert werden.')
            return render(request, 'report_edit_qm.html', {
                'page_title': 'Korrekturmeldung bearbeiten',
                'form': form,
                'report': report,
                'role': get_user_role(request.user),
                'users': get_qm_users()
            })
    else:
        report = CorrectionReport.objects.get(id=id)

        return render(request, 'report_edit_qm.html', {
            'page_title': 'Korrekturmeldung bearbeiten',
            'form': CorrectionReportQMForm(instance=report),
            'report': report,
            'role': get_user_role(request.user),
            'users': get_qm_users()
        })


@login_required
def assign_report(request):
    if not roles_are_valid(request, [Roles.QM_MANAGER.value, Roles.QM_LEADER.value]):
        return redirect(reports_all_view)

    if request.method == 'POST':
        report = CorrectionReport.objects.get(id=request.POST['report_id'])

        if request.POST['assignee_id'] == '':
            if report.assigned_to is None:
                assignee = None
            else:
                assignee = report.assigned_to
        else:
            assignee = User.objects.get(id=request.POST['assignee_id'])

        if request.POST['manager_id'] == '':
            manager = request.user
        else:
            manager = User.objects.get(id=request.POST['manager_id'])

        if report is not None:
            CorrectionReport.objects.filter(id=report.id).update(
                qm_manager=manager,
                assigned_at=datetime.now(),
                assigned_to=assignee,
                edited_at=datetime.now(),
                report_status=CorrectionReport.ReportStatus.ASSIGNED
            )
            messages.success(request, f'Die Korrekturmeldung wurde erfolgreich an {assignee.username} zugewiesen.')
            return redirect(reports_detail_view, id=report.id)
        else:
            messages.error(request, f'Die Korrekturmeldung konnte nicht zugewiesen werden.')
            return redirect(reports_detail_view, id=report.id)


@login_required
def delete_report(request, id):
    if request.method == "POST":
        report = CorrectionReport.objects.get(id=id)
        title = report.title
        confirmation_text = request.POST['confirmation_text']

        if request.user != report.created_by:
            messages.error(request, f"Du bist nicht der Ersteller dieser Korrekturmeldung.")
            return redirect(reports_all_view)

        if confirmation_text == title:
            report.delete()
            messages.success(request, f"Die Korrekturmeldung {title} wurde erfolgreich gelöscht.")
            return redirect(reports_all_view)
        else:
            messages.warning(request, f"\"{confirmation_text}\" stimmt nicht mit dem Titel der Korrekturmeldung "
                                      f"\"{title}\" überein und konnte deshalb nicht gelöscht werden")
            return redirect(reports_detail_view, id=id)
