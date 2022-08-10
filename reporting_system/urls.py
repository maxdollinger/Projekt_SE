from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("add", views.add_correction_report, name="add_correction_report"),
]