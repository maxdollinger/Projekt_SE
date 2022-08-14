from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from reporting_system.forms import CustomLoginForm

urlpatterns = [
    path("add", views.add_correction_report, name="add_correction_report"),
    path("team", views.team, name="Team")
    path("overview", views.overview, name="Overview"),
        authentication_form=CustomLoginForm), name="Login"),
        template_name="index.html",
    path("", auth_views.LoginView.as_view(
]