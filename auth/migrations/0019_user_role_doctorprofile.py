# Generated by Django 5.1 on 2024-10-30 11:31

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0018_user_code'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='role',
            field=models.CharField(choices=[('doctor', 'Doctor'), ('patient', 'Patient')], default='patient', help_text='Specify if the user is a doctor or a patient', max_length=20),
        ),
        migrations.CreateModel(
            name='DoctorProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('specialization', models.CharField(blank=True, max_length=100)),
                ('license_number', models.CharField(blank=True, max_length=50)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='doctor_profile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]