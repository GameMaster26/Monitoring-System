# Generated by Django 5.1 on 2024-09-15 13:07

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('monitoring', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='history',
            name='brgy_id',
            field=models.ForeignKey(db_column='brgy_id', default=20, on_delete=django.db.models.deletion.CASCADE, related_name='history_brgy', to='monitoring.barangay', verbose_name='Barangay Exposure'),
        ),
        migrations.AlterField(
            model_name='history',
            name='muni_id',
            field=models.ForeignKey(db_column='muni_id', default=3, on_delete=django.db.models.deletion.CASCADE, related_name='history_muni', to='monitoring.municipality', verbose_name='Municipality of Exposure'),
        ),
        migrations.AlterField(
            model_name='patient',
            name='brgy_id',
            field=models.ForeignKey(default=20, on_delete=django.db.models.deletion.CASCADE, related_name='patients_brgy', to='monitoring.barangay', verbose_name='Barangay'),
        ),
        migrations.AlterField(
            model_name='patient',
            name='muni_id',
            field=models.ForeignKey(default=3, on_delete=django.db.models.deletion.CASCADE, related_name='patients_muni', to='monitoring.municipality', verbose_name='Municipality'),
        ),
    ]
