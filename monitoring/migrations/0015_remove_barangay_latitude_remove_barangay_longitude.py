# Generated by Django 5.0.6 on 2024-08-23 13:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('monitoring', '0014_barangay_latitude_barangay_longitude_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='barangay',
            name='latitude',
        ),
        migrations.RemoveField(
            model_name='barangay',
            name='longitude',
        ),
    ]
