# Generated by Django 3.2.15 on 2022-09-05 21:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reporting_system', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='correctionreport',
            name='comment',
            field=models.TextField(blank=True, null=True, verbose_name='Kommentar'),
        ),
    ]