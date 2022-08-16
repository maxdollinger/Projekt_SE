from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from reporting_system.forms.login_form import CustomLoginForm

urlpatterns = [
    path("add", views.add_correction_report, name="add_correction_report"),
    path("", auth_views.LoginView.as_view(
    template_name="index.html",
    authentication_form=CustomLoginForm), name="Login"),
    path("overview", views.overview, name="Overview"),
    path("team", views.team, name="Team")
]