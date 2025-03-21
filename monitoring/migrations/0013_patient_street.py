# Generated by Django 5.1 on 2024-12-15 12:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('monitoring', '0012_doctor_is_superdoctor'),
    ]

    operations = [
        migrations.AddField(
            model_name='patient',
            name='street',
            field=models.CharField(blank=True, choices=[('Abad Street', 'Abad Street'), ('Adobo Compound Road', 'Adobo Compound Road'), ('Ballesteros Street', 'Ballesteros Street'), ('Biliran Circumferential Road', 'Biliran Circumferential Road'), ('Biliran Rotunda', 'Biliran Rotunda'), ('Bonifacio Street', 'Bonifacio Street'), ('Burgos Street', 'Burgos Street'), ('Cabadiangan Road', 'Cabadiangan Road'), ('Calambis Bridge', 'Calambis Bridge'), ('Caneja Street', 'Caneja Street'), ('Castin Street', 'Castin Street'), ('Corvera Street', 'Corvera Street'), ('Garrido', 'Garrido'), ('Gomez', 'Gomez'), ('Imelda Road', 'Imelda Road'), ('Jaguros Street', 'Jaguros Street'), ('Leyte-Biliran Road', 'Leyte-Biliran Road'), ('Lico Road', 'Lico Road'), ('Limpiado', 'Limpiado'), ('Lomboy Road', 'Lomboy Road'), ('Looc Diversion Road', 'Looc Diversion Road'), ('Mabini Pier', 'Mabini Pier'), ('Mabini Street', 'Mabini Street'), ('Magallanes Street', 'Magallanes Street'), ('Mapuyo Loop', 'Mapuyo Loop'), ('Maripipi Circumferential Road', 'Maripipi Circumferential Road'), ('Mission', 'Mission'), ('Naval-Caibiran Cross Country Road', 'Naval-Caibiran Cross Country Road'), ('Padre Garcia Street', 'Padre Garcia Street'), ('Padre Innocentes Street', 'Padre Innocentes Street'), ('Real Street', 'Real Street'), ('Redaza Street', 'Redaza Street'), ('Rizal Street', 'Rizal Street'), ('Rojas Street', 'Rojas Street'), ('Sabenorio Street', 'Sabenorio Street'), ('Salazar', 'Salazar'), ('Salut', 'Salut'), ('San Isidro Street', 'San Isidro Street'), ('San Juan Street', 'San Juan Street'), ('San Roque Street', 'San Roque Street'), ('Santa Cruz Street', 'Santa Cruz Street'), ('Santissimo Rosario', 'Santissimo Rosario'), ('Santo Niño Road', 'Santo Niño Road'), ('Sitio Hayahay Road', 'Sitio Hayahay Road'), ('Sitio Lupa Road', 'Sitio Lupa Road'), ('Vicentillo Extension', 'Vicentillo Extension'), ('Vicentillo Street', 'Vicentillo Street'), ('Zamora', 'Zamora')], max_length=100, null=True),
        ),
    ]
