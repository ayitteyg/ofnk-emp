# Generated by Django 4.1 on 2022-10-18 12:43

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('username', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('fullname', models.CharField(max_length=30, verbose_name='Full Name')),
                ('gender', models.CharField(choices=[('M', 'Male'), ('F', 'Female')], max_length=7, verbose_name='Gender')),
                ('contact', models.CharField(blank=True, max_length=10, null=True, verbose_name='Contact')),
                ('dob', models.DateField(blank=True, null=True, verbose_name='Date of birth')),
                ('loc', models.CharField(blank=True, max_length=20, null=True, verbose_name='Location')),
                ('gname', models.CharField(blank=True, max_length=30, null=True, verbose_name="Guarantor's Name")),
                ('gcontact', models.CharField(blank=True, max_length=10, null=True, verbose_name="Guarantor's contact")),
                ('job', models.CharField(blank=True, choices=[('Site Manager', 'Site Manager'), ('Asst. Manager', 'Asst. Manager'), ('Supervisor', 'Supervisor'), ('Quality Marshal', 'Quality Marshal'), ('Pump Attendant', 'Pump Attendant'), ('Shop Attendant', 'Shop Attendant'), ('Cleaner', 'Cleaner'), ('Security', 'Security'), ('Driver', 'Driver'), ('Lube Technician', 'Lube Technician'), ('Oil Specialist', ' Oil Specialist')], max_length=30, null=True, verbose_name='Job Description')),
                ('date_employed', models.DateField(blank=True, null=True, verbose_name='Year Employed')),
                ('ssnit', models.CharField(blank=True, max_length=15, null=True, verbose_name='Ssnit Number')),
                ('bank', models.CharField(blank=True, max_length=15, null=True, verbose_name='Account Number')),
                ('group', models.CharField(choices=[('management', 'management'), ('staff', 'staff'), ('trainee', 'trainee')], max_length=20, verbose_name='Group')),
            ],
        ),
        migrations.CreateModel(
            name='Resources',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('filename', models.CharField(max_length=20, verbose_name='File Name')),
                ('file', models.FileField(upload_to='RscFiles/')),
            ],
        ),
        migrations.CreateModel(
            name='MsgSent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject', models.CharField(max_length=100)),
                ('message', models.TextField(max_length=3000)),
                ('date_sent', models.DateField(auto_now_add=True)),
                ('sent_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='by', to=settings.AUTH_USER_MODEL)),
                ('sent_to', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='to', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Letters',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('action', models.CharField(choices=[('Permission', 'Permission'), ('Verbal Warning', 'Verbal Warning'), ('Suspension', 'Suspension'), ('Dismissal', 'Dismissal'), ('Query Letter', 'Query Letter')], max_length=30, verbose_name='Action')),
                ('description', models.TextField(max_length=1000, verbose_name='Description')),
                ('date', models.DateField(auto_now_add=True)),
                ('authorized', models.CharField(choices=[('Manager', 'Manager'), ('Supervisor', 'Supervisor'), ('QM', 'Quality Marshal')], max_length=30, verbose_name='Given by')),
                ('start_from', models.DateField(blank=True, null=True, verbose_name='Start From')),
                ('end', models.DateField(blank=True, null=True, verbose_name='Ending')),
                ('file', models.FileField(upload_to='LtrsFiles/')),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]