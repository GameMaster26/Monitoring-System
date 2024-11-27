# Generated by Django 5.1 on 2024-11-13 16:04

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('monitoring', '0005_alter_doctor_brgy_id_alter_history_brgy_id_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='doctor',
            name='brgy_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='doctors_brgy', to='monitoring.barangay', verbose_name='Barangay'),
        ),
        migrations.AlterField(
            model_name='history',
            name='brgy_id',
            field=models.ForeignKey(db_column='brgy_id', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='history_brgy', to='monitoring.barangay', verbose_name='Barangay Exposure'),
        ),
        migrations.AlterField(
            model_name='history',
            name='source_of_exposure',
            field=models.CharField(choices=[('Dog', 'Dog'), ('Cat', 'Cat'), ('Bat', 'Bat'), ('Monkey', 'Monkey'), ('Human', 'Human'), ('Horse', 'Horse'), ('Cow', 'Cow'), ('Goat', 'Goat'), ('Pig', 'Pig'), ('Rabbit', 'Rabbit'), ('Guinea Pig', 'Guinea Pig')], max_length=10, verbose_name='Animal'),
        ),
        migrations.AlterField(
            model_name='patient',
            name='brgy_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='patients_brgy', to='monitoring.barangay', verbose_name='Barangay'),
        ),
    ]
