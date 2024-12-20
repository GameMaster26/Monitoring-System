# Generated by Django 5.1 on 2024-11-15 01:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('monitoring', '0008_alter_history_date_of_exposure'),
    ]

    operations = [
        migrations.AlterField(
            model_name='treatment',
            name='day0',
            field=models.DateField(blank=True, null=True, verbose_name='Day 0(First Dose)'),
        ),
        migrations.AlterField(
            model_name='treatment',
            name='day3',
            field=models.DateField(blank=True, null=True, verbose_name='Day 3(Second Dose)'),
        ),
        migrations.AlterField(
            model_name='treatment',
            name='day7',
            field=models.DateField(blank=True, null=True, verbose_name='Day 7(Third Dose)'),
        ),
        migrations.AlterField(
            model_name='treatment',
            name='remarks',
            field=models.CharField(blank=True, choices=[('Completed', 'Completed'), ('Not Started', 'Not Started'), ('No Show', 'No Show'), ('Aggressive Behavior Noted', 'Aggressive Behavior Noted'), ('Animal Captured', 'Animal Captured'), ('Animal Deceased', 'Animal Deceased'), ('Animal Not Captured', 'Animal Not Captured'), ('Animal Not Observed', 'Animal Not Observed'), ('Animal Observed', 'Animal Observed'), ('Animal Quarantined', 'Animal Quarantined'), ('Animal Released', 'Animal Released'), ('Animal Unvaccinated', 'Animal Unvaccinated'), ('Animal Unknown', 'Animal Unknown'), ('Animal Vaccinated', 'Animal Vaccinated'), ('Owner Cooperating', 'Owner Cooperating'), ('Owner Not Cooperating', 'Owner Not Cooperating'), ('Owner Not Found', 'Owner Not Found'), ('Pet Animal', 'Pet Animal'), ('Rabies Suspected', 'Rabies Suspected'), ('Rabies Test Negative', 'Rabies Test Negative'), ('Rabies Test Pending', 'Rabies Test Pending'), ('Rabies Test Positive', 'Rabies Test Positive'), ('Stray Animal', 'Stray Animal'), ('Unknown Animal', 'Unknown Animal'), ('Additional Treatment Needed', 'Additional Treatment Needed'), ('Awaiting Vaccine', 'Awaiting Vaccine'), ('Canceled', 'Canceled'), ('Discontinued', 'Discontinued'), ('Follow-Up Required', 'Follow-Up Required'), ('In Observation', 'In Observation'), ('In Progress', 'In Progress'), ('Partially Completed', 'Partially Completed'), ('Pending', 'Pending'), ('Referred to Specialist', 'Referred to Specialist'), ('Vaccination Scheduled', 'Vaccination Scheduled')], max_length=100, null=True, verbose_name='Remarks'),
        ),
    ]
