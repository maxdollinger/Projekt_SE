from django.contrib import admin
from .models import CorrectionReport
# Register your models here.
@admin.register(CorrectionReport)
class CorrectionReportAdmin(admin.ModelAdmin):
    pass