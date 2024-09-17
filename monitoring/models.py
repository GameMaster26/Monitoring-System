from django import forms
from django.db import models
from datetime import datetime,date,timedelta
import os, random
from django.utils.html import mark_safe
from django.utils import timezone
from django.contrib import admin
from django.db.models import Q  
from functools import reduce  
import operator
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.core.validators import RegexValidator
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.db.models import Max
from django.contrib.gis.db import models
from django.contrib.gis.db import models as geomodels
from django.db.models.signals import post_save
from django.db.models import OuterRef, Subquery

class Municipality(models.Model):
    muni_id = models.AutoField(primary_key=True)
    muni_name = models.CharField(max_length=100, verbose_name="Municipality Name")
    geom = geomodels.MultiPolygonField(verbose_name="Geom", null=True, blank=True)

    @property
    def latitude(self):
        return self.geom.y if self.geom else None

    @property
    def longitude(self):
        return self.geom.x if self.geom else None
    
    def __str__(self):
        return f"{self.muni_name}"
    class Meta:
        verbose_name_plural = "Municipalities"

class Barangay(models.Model):
    brgy_id = models.AutoField(primary_key=True)
    brgy_name = models.CharField(max_length=100, verbose_name="Barangay Name")
    muni_id = models.ForeignKey(Municipality, on_delete=models.CASCADE, verbose_name="Municipality Name",default=9, related_name='barangays',db_column='muni_id')
    #tmp_muni = models.CharField(max_length=100, verbose_name="Tmp muni",)
    """ latitude = models.DecimalField(verbose_name="Latitude" ,max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(verbose_name="Longitude" ,max_digits=9, decimal_places=6, null=True, blank=True) """
    #geom= models.GeometryField(verbose_name="Geometry", null=True, blank=True)

    def save(self, *args, **kwargs):
        self.brgy_name = self.brgy_name.title()  # Capitalize first letter
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.brgy_name}, {self.muni_id.muni_name}"

    class Meta:
        verbose_name_plural = "Barangays"
        # Enforce uniqueness for the combination of brgy_name and muni_id
        unique_together = ['brgy_name', 'muni_id']  

def validate_contact_number(value):
    if not value.startswith('09') or len(value) != 11:
        raise ValidationError(
            _('Invalid contact number: %(value)s. It should start with "09" and be 11 digits long.'),
            params={'value': value},
        )
    
class Patient(models.Model):
    app_label = 'monitoring'

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="User", related_name='patients')
    patient_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=200, verbose_name="First Name", blank=False,)
    last_name = models.CharField(max_length=200, verbose_name="Last Name", blank=False)
    muni_id = models.ForeignKey(Municipality, on_delete=models.CASCADE, verbose_name="Municipality",default=1, related_name='patients_muni')#7 cabucgayan,6 culaba, 5 almeria, 8 kaw
    brgy_id = models.ForeignKey(Barangay, on_delete=models.CASCADE, verbose_name="Barangay",default=11, related_name='patients_brgy')#88 Caib, 50 cabuc, 47 kaw, 67 cula
    birthday = models.DateField(verbose_name="Birthday", default=date(2001, 12, 2))
    sex_choice =(
        ('male','Male'),
        ('female','Female'),
    )
    sex = models.CharField(choices=sex_choice, max_length=20,default='male', verbose_name="Sex")
    contactNumber = models.CharField(max_length=12, blank=False, verbose_name="Contact Number",validators=[validate_contact_number],default= '09582488441',)   

    def save(self, *args, **kwargs):
        self.first_name = self.first_name.title()  # Capitalize first letter
        self.last_name = self.last_name.title()  
        super().save(*args, **kwargs)
    
    def code(self):
        return self.user.username
    code.short_description = 'Username'

    """ def registration_no(self):
        history = History.objects.filter(patient_id=self.patient_id).first()
        return history.registration_no if history else 'N/A' """

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    class Meta:
        
        #ordering = ['-patient_id__registration_no']
        verbose_name_plural = "Patients"

class History(models.Model):

    history_id = models.AutoField(primary_key=True)
    patient_id = models.ForeignKey(Patient, on_delete=models.CASCADE, verbose_name="Patient", related_name='histories',db_column='patient_id')
    registration_no = models.CharField(max_length=200,verbose_name='Registration Number', blank=True, null=True,)#unique=True, 
    #treatment_id = models.ForeignKey(Treatment, on_delete=models.CASCADE, verbose_name="Treatment",default=1,  related_name='history_treatment', db_column='treatment_id')
    date_registered = models.DateField(default=date(2024,9,1),verbose_name="Date Registered")
    date_of_exposure = models.DateField(blank=True, null=True,default=date(2024, 8, 16), verbose_name="Date of Exposure")
    muni_id = models.ForeignKey(Municipality, on_delete=models.CASCADE, verbose_name="Municipality of Exposure",default=1, related_name='history_muni',db_column='muni_id')
    brgy_id = models.ForeignKey(Barangay, on_delete=models.CASCADE, verbose_name="Barangay Exposure",default=11, related_name='history_brgy',db_column='brgy_id')
    
    category = (
        ('I','I'),
        ('II',"II"),
        ('III','III'),
    )
    category_of_exposure = models.CharField(max_length=10, choices=category,default="II",verbose_name="Exposure Category" )

    source_of_exposure_choices = (
        ('Dog', 'Dog'),
        ('Cat', 'Cat'),
        ('Others', 'Others'),
    )
    exposure_type_choices = (
        ('Bite', 'Bite'),
        ('Non-Bite', 'Non-Bite'),
    )
    provoked_choices = (
        ('Provoked', 'Provoked'),
        ('Unprovoked', 'Unprovoked'),
    )
    immunization_choices = (
        ('Immunized', 'Immunized'),
        ('Unimmunized', 'Unimmunized'),
    )
    status_of_animal_choices = (
        ('Alive','Alive'),
        ('Dead','Dead'),
        ('Killed','Killed'),
        ('Lost','Lost'),
    )
    animal_status = (
        ('Stray','Stray'),
        ('Leashed/Caged','Leashed/Caged'),
    )
    
    washing = (
        ('Yes','Yes'),
        ('No','No'),
    )
    source_of_exposure = models.CharField(max_length=10 ,choices=source_of_exposure_choices,default='Cat',  blank=False, verbose_name="Animal")
    exposure_type = models.CharField(max_length=10, choices=exposure_type_choices, default='Bite', blank=False, verbose_name="Type of Exposure")
    bite_site = models.CharField(max_length=100,blank=False,default='right thigh', verbose_name="Bite Site")
    provoked_status = models.CharField(max_length=20, choices=provoked_choices,default='Unprovoked' ,verbose_name="Provocation Status")
    immunization_status = models.CharField(max_length=20, choices=immunization_choices,default='Unimmunized', verbose_name="Animal Vaccination")
    status_of_animal = models.CharField(max_length=20,choices=status_of_animal_choices,blank=False,default='Lost', verbose_name="Animal Status")
    confinement_status = models.CharField(max_length=20,choices=animal_status,blank=False,default='Stray', verbose_name="Confinement Status")
    
    washing_hands = models.CharField(max_length=10,choices=washing,default='Yes' ,verbose_name="Washing Wound") 
    latitude = models.FloatField(verbose_name="Latitude", blank=True, null=False, default=0.0)
    longitude = models.FloatField(verbose_name="Longitude", blank=True, null=False, default=0.0)
    geom= geomodels.PointField(verbose_name="Geometry",  null=False, blank=False)



    def save(self, *args, **kwargs):
        if self.geom:
            # Automatically set latitude and longitude from geom if geom is set
            self.latitude = self.geom.y
            self.longitude = self.geom.x
        else:
            # Ensure latitude and longitude are set
            if self.latitude is None or self.longitude is None:
                raise ValueError("Both latitude and longitude must be set if geom is not provided.")
        
        if not self.registration_no:
            self.registration_no = self.generate_registration_no()
        self.registration_no = self.registration_no.upper()  # Convert to uppercase
        self.bite_site = self.bite_site.title()  # Capitalize first letter
        super().save(*args, **kwargs)

    def generate_registration_no(self):
        current_year = date.today().year
        user_id = self.patient_id.user.id
    
        # Filter histories for the current year and user, and get the last registration number
        last_history = History.objects.filter(
            patient_id__user__id=user_id,
            registration_no__startswith=f'{current_year}-'
        ).order_by('registration_no').last()

        if last_history:
            last_reg_no = last_history.registration_no
            last_reg_num = int(last_reg_no.split('-')[-1])
            new_reg_num = last_reg_num + 1
        else:
            new_reg_num = 1

        new_registration_no = f'{current_year}-{new_reg_num:05d}'
        return new_registration_no

    def get_search_results(self, request, queryset, search_term):
        queryset, use_distinct = super().get_search_results(request, queryset, search_term)

        if search_term:
            # Specify the fields you want to search for names
            search_fields = ['patient_id__first_name', 'patient_id__last_name']
            
            # Split the search term into individual characters
            terms = search_term.strip().split()
            for term in terms:
                or_queries = [Q(**{f'{field}__icontains': term}) for field in search_fields]
                queryset = queryset.filter(reduce(operator.or_, or_queries))

        return queryset, use_distinct
    
    def code(self):
        return self.patient_id.user.username
    code.short_description = 'Username'

    def __str__(self):
        return '{} - Registered on {} - Source: {}'.format(
            self.patient_id,
            self.date_registered,
            self.source_of_exposure
            )
    
    class Meta:
        verbose_name_plural = "Patient's History"
        ordering = ['-registration_no']
        unique_together = ('registration_no', 'patient_id')  # Ensure registration_no is unique per patient


class Treatment(models.Model):
    
    treatment_id = models.AutoField(primary_key=True)
    patient_id = models.ForeignKey(Patient, on_delete=models.CASCADE, verbose_name="Patient", related_name='treatments_patient', db_column='patient_id')
    #history_id = models.ForeignKey(History, on_delete=models.CASCADE,s verbose_name="History", related_name='treatment_history', db_column='history_id')
    

    GENERIC_NAME = (
        ('PCECCV', 'PCECCV'),
        ('PVRV', 'PVRV'),
    )
    BRAND_NAME = (
        ('Verorab', 'Verorab'),
        ('Speeda', 'Speeda'),
        ('Vaxirab', 'Vaxirab'),
        ('Abhayrab', 'Abhayrab'),
    )
    route = (
        ('intramuscular', 'Intramuscular'),
        ('intradermal', 'Intradermal')
    )
    vaccine_generic_name = models.CharField(max_length=10, choices=GENERIC_NAME, default='PCECCV', verbose_name='Vaccine Generic Name')  # PCECCV or PVRV
    vaccine_brand_name = models.CharField(max_length=10, choices=BRAND_NAME,default='Vaxirab', verbose_name='Vaccine Brand Name')  # Verorab, Speeda, etc.
    vaccine_route = models.CharField(max_length=50, choices=route, default='intradermal', verbose_name='Vaccine Route')  # Route of administration

    day0 = models.DateField(default=date(2024,9,4), blank=True, null=True, verbose_name="Day 0")#default=date(2024,4,3),
    day0_arrived = models.BooleanField(default=False, verbose_name="") 

    day3 = models.DateField(default=date(2024,9,7), blank=True, null=True, verbose_name="Day 3")#default=date(2024,4,6),
    day3_arrived = models.BooleanField(default=False, verbose_name="")

    day7 = models.DateField(default=date(2024,9,11),blank=True, null=True, verbose_name="Day 7")#default=day7_str, default=date(2024,4,10), 
    day7_arrived = models.BooleanField(default=False, verbose_name="")

    day14 = models.DateField(blank=True, null=True, verbose_name="Day 14")
    
    day28 = models.DateField(blank=True, null=True, verbose_name="Day 28")
    day28_arrived = models.BooleanField(default=False, verbose_name="")

    rig_given = models.DateField(blank=True, null=True, verbose_name="RIG")

    animal_alive = models.BooleanField(default=True, null=True, verbose_name='Animal alive')
    remarks = models.TextField(blank=True)

    def code(self):
        return self.patient_id.user.username
    code.short_description = 'Username'

    def __str__(self):
        return f"Treatment for {self.patient_id.first_name} {self.patient_id.last_name}"
    
    def get_category_of_exposure(self):
        history = History.objects.filter(patient_id=self.patient_id).first()
        return history.category_of_exposure if history else 'N/A'
    
    def registration_no(self):
        history = History.objects.filter(patient_id=self.patient_id).first()
        return history.registration_no if history else 'N/A'
    registration_no.short_description = "Registration Number"

    class Meta:
        ordering = ['-patient_id']
        verbose_name_plural = "Patient's Treatment"