# Generated by Django 5.1 on 2024-11-25 22:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('monitoring', '0011_alter_treatment_remarks'),
    ]

    operations = [
        migrations.AddField(
            model_name='doctor',
            name='is_superdoctor',
            field=models.BooleanField(default=False, verbose_name='Lead  Doctor'),
        ),
    ]