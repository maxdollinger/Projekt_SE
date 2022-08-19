from django.urls import path
from . import views

urlpatterns = [
    path("", views.reports_all_view, name="reports"),
    path("add", views.add_correction_report, name="add_correction_report"),
    path("edit/<int:id>", views.edit_correction_report, name="edit_correction_report"),
    path("reports", views.reports_all_view, name="reports"),
    path("detail/<int:id>", views.reports_detail_view, name="reports_detail"),
]
