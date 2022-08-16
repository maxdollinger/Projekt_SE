"""correction_management_system URL Configuration

The `urlpatterns` list routes URLs to controller. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function controller
    1. Add an import:  from my_app import controller
    2. Add a URL to urlpatterns:  path('', controller.home, name='home')
Class-based controller
    1. Add an import:  from other_app.controller import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from reporting_system import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', include("reporting_system.urls")),
    path('admin/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

