from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path("", auth_views.LoginView.as_view(template_name="index.html")),
    path("team", views.team, name="team")
]