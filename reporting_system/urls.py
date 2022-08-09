from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path("", auth_views.LoginView.as_view(template_name="index.html")),
    path("accounts/", include("django.contrib.auth.urls")),
    path("team", views.team, name="team")
]