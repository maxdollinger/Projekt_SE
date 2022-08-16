# Generated by Django 4.1 on 2022-08-15 08:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CorrectionReport',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('created_at', models.DateField(default='2022-08-15')),
                ('assigned_at', models.DateField(default=None)),
                ('edited_at', models.DateField(default=None)),
                ('document_name', models.CharField(max_length=255)),
                ('course', models.CharField(max_length=255)),
                ('report_status', models.CharField(choices=[('1', 'Gemeldet'), ('2', 'Zugewiesen'), ('3', 'In Bearbeitung'), ('4', 'Bearbeitet'), ('5', 'Abgewiesen')], default='1', max_length=2)),
                ('report_type', models.CharField(choices=[('1', 'Hinweis'), ('2', 'Warnung'), ('3', 'Error'), ('4', 'Fatal')], default='1', max_length=2)),
            ],
        ),
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('file_name', models.CharField(max_length=255)),
                ('pdf', models.FileField(upload_to='pdf')),
                ('correction_report', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='reporting_system.correctionreport')),
            ],
        ),
    ]
