from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from reporting_system.forms.login_form import CustomLoginForm

urlpatterns = [
    path("", auth_views.LoginView.as_view(
        redirect_authenticated_user=True,
        template_name="index.html",
        authentication_form=CustomLoginForm), name="index"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("add", views.add_correction_report, name="add_correction_report"),
    path("reports", views.reports_view, name="reports"),
    path("team", views.team, name="team")
]
