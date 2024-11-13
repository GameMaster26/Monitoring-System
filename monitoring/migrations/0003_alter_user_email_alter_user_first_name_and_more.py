# Generated by Django 5.1 on 2024-11-12 00:56

import monitoring.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('monitoring', '0002_alter_doctor_specialization'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(max_length=254, verbose_name='email address'),
        ),
        migrations.AlterField(
            model_name='user',
            name='first_name',
            field=models.CharField(max_length=150, verbose_name='first name'),
        ),
        migrations.AlterField(
            model_name='user',
            name='last_name',
            field=models.CharField(max_length=150, verbose_name='last name'),
        ),
        migrations.AlterField(
            model_name='user',
            name='number',
            field=models.CharField(max_length=12, validators=[monitoring.models.validate_contact_number], verbose_name='Contact Number'),
        ),
    ]