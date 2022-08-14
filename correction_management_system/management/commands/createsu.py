from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
import os

class Command(BaseCommand):

    def handle(self, *args, **options):
        if not User.objects.filter(username="admin").exists():
            User.objects.create_superuser(os.environ["ADMIN_NAME"], "admin@admin.com", os.environ["ADMIN_PASSWORD"])