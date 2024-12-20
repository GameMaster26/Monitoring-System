# Generated by Django 5.1 on 2024-11-11 15:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('monitoring', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='doctor',
            name='specialization',
            field=models.CharField(blank=True, choices=[('gp', 'General Practitioner'), ('pediatrician', 'Pediatrician'), ('dermatologist', 'Dermatologist'), ('cardiologist', 'Cardiologist'), ('orthopedic', 'Orthopedic Surgeon'), ('obgyn', 'Obstetrician/Gynecologist'), ('endocrinologist', 'Endocrinologist'), ('neurologist', 'Neurologist'), ('ophthalmologist', 'Ophthalmologist'), ('psychiatrist', 'Psychiatrist')], null=True, verbose_name='Specialization'),
        ),
    ]
