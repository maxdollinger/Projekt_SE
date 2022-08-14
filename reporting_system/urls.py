from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from reporting_system.forms import CustomLoginForm

urlpatterns = [
    path("", auth_views.LoginView.as_view(
        template_name="index.html",
        authentication_form=CustomLoginForm), name="Login"),
    path("overview", views.overview, name="Overview"),
    path("team", views.team, name="Team")
]