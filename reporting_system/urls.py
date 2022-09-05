from django.urls import path
from . import views

urlpatterns = [
    path("", views.reports_all_view, name="reports"),
    path("add", views.add_correction_report, name="add_correction_report"),
    path("edit-student/<int:id>", views.edit_report_student, name="edit_report_student"),
    path("edit-emp/<int:id>", views.edit_report_emp, name="edit_report_emp"),
    path("edit-qm/<int:id>", views.edit_report_qm, name="edit_report_qm"),
    path("assign", views.assign_report, name="assign_report"),
    path("reports", views.reports_all_view, name="reports"),
    path("detail/<int:id>", views.reports_detail_view, name="reports_detail"),
]
