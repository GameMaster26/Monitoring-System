# Generated by Django 5.0.6 on 2024-08-06 06:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('monitoring', '0007_remove_municipality_latitude_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='barangay',
            name='street',
            field=models.CharField(default='Zone 4', max_length=100, verbose_name='Street'),
        ),
    ]