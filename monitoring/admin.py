from django.contrib import admin
from datetime import datetime,timedelta
from .models import Patient,History,Treatment,Municipality,Barangay,User
from django.contrib.contenttypes.admin import GenericTabularInline,GenericInlineModelAdmin,GenericInlineModelAdminChecks,GenericStackedInline
from django.contrib.auth.models import Group, User
from django import forms
from django.http import HttpResponseRedirect
from django.urls import reverse
import django.apps
from django.contrib.admin.models import LogEntry
from .forms import PatientAdminForm, HistoryAdminForm,HistoryForm,HistoryInlineForm
from django.contrib.auth.admin import UserAdmin,GroupAdmin
from django.db.models import Max,OuterRef, Subquery

# admin.py
from django.contrib.admin import AdminSite
from django.urls import path
from . import views

""" class CustomAdminSite(AdminSite):
    site_header = 'My Admin'

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('downloads/', self.admin_view(views.table), name='admin_downloads'),
        ]
        return custom_urls + urls

custom_admin_site = CustomAdminSite(name='custom_admin')
 """



class PatientInline(admin.StackedInline):

    

    model = Patient
    extra = 0
    
    def get_readonly_fields(self, request, obj=None):
        if request.user.is_superuser:
            readonly_fields = [field.name for field in self.model._meta.fields if field.name != 'patient_id']
            return readonly_fields
        return self.readonly_fields

class HistoryInline(admin.StackedInline):
    model = History
    extra = 0
    fields = ('date_registered', 'date_of_exposure','muni_id','brgy_id', 'source_of_exposure', 'exposure_type', 'bite_site','provoked_status', 'immunization_status','status_of_animal', 'confinement_status', 'category_of_exposure')
    
    def get_formset(self, request, obj=None, **kwargs):
        formset = super().get_formset(request, obj, **kwargs)
        # Remove registration_no field from inline form
        formset.form.base_fields.pop('registration_no', None)
        return formset
    
    def get_readonly_fields(self, request, obj=None):
        if request.user.is_superuser:
            readonly_fields = [field.name for field in self.model._meta.fields if field.name != 'id']
            return readonly_fields
        return self.readonly_fields
    
    

class TreatmentInline(admin.StackedInline):
    model = Treatment
    extra = 0


class AgeFilter(admin.SimpleListFilter):
    title = 'Age'  # Displayed title for the filter
    parameter_name = 'age'  # URL parameter name for the filter

    def lookups(self, request, model_admin):
        # Define filter options
        return (
            ('below_15', 'Below or Equal 15'),
            ('above_16', 'Above 15'),
        )

    def queryset(self, request, queryset):
        # Apply filter based on selected option
        today = datetime.today()
        if self.value() == 'below_15':
            return queryset.filter(birthday__gt=today - timedelta(days=365*15))
        elif self.value() == 'above_16':
            return queryset.filter(birthday__lt=today - timedelta(days=365*16))

class BarangayFilter(admin.SimpleListFilter):
    title = 'Barangay'
    parameter_name = 'brgy_id'
    

    def lookups(self, request, model_admin):
        # Retrieve distinct barangay names from the Patient model
        return Patient.objects.values_list('brgy_id__brgy_name', 'brgy_id__brgy_name').distinct()

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(brgy_id__brgy_name=self.value())

class MunicipalityFilter(admin.SimpleListFilter):
    title = 'Municipality'
    parameter_name = 'muni_id'

    def lookups(self, request, model_admin):
        # Retrieve distinct municipality names from the Patient model
        return Patient.objects.values_list('muni_id__muni_name', 'muni_id__muni_name').distinct()

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(muni_id__muni_name=self.value())

@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    
    #form = HistoryForm
    
    list_display = ('code','registration_no',  'first_name','last_name', 'brgy_id','muni_id','age', 'sex','contactNumber', )  # Changed 'birthday' to 'get_age'
    list_per_page = 10
    search_fields = ['first_name','last_name',]
    list_filter = ('user__code', AgeFilter,BarangayFilter,MunicipalityFilter,)  # Changed 'birthday' to 'get_age'
    inlines = [HistoryInline, TreatmentInline] 
    #list_display_links = ['code',]
    exclude = ('registration_no','user',) 
    ordering = ('-patient_id',) 

    

    def brgy_name(self, obj):
        return obj.brgy_id.brgy_name
    brgy_name.short_description = 'Barangay'

    def muni_name(self, obj):
        return obj.muni_id.muni_name
    muni_name.short_description = 'Municipality'
    
    def age(self, obj):
        # Calculate age based on the birth date
        today = datetime.today()
        age = today.year - obj.birthday.year - ((today.month, today.day) < (obj.birthday.month, obj.birthday.day))
        return age
    age.short_description = 'Age'  # Display as 'Age' in the admin interface

    def registration_no(self, obj):
        return obj.registration_no()
    registration_no.short_description = 'Registration Number'
    
    def get_list_display(self, request):
        if request.user.is_superuser:
            return self.list_display
        return ('registration_no', 'first_name','last_name', 'brgy_id','muni_id','age', 'sex','contactNumber', )

    def get_list_filter(self, request):
        if request.user.is_superuser:
            return self.list_filter
        return (AgeFilter, BarangayFilter, MunicipalityFilter)

    def get_readonly_fields(self, request, obj=None):
        if request.user.is_superuser:
            readonly_fields = [field.name for field in self.model._meta.fields if field.name != 'patient_id']
            return readonly_fields
        return self.readonly_fields

    def has_add_permission(self, request):
        if request.user.is_superuser:
            return False
        return super().has_add_permission(request)

    def has_delete_permission(self, request, obj=None):
        if request.user.is_superuser:
            return False
        return super().has_delete_permission(request, obj)
    
    def has_change_permission(self,request,obj=None):
        if request.user.is_superuser:
            return False
        return super().has_change_permission(request,obj)
    
    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.user = request.user
        super().save_model(request, obj, form, change)

    """ def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(user=request.user) """
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            queryset = qs.annotate(
                latest_registration_no=Max('histories__registration_no')
            ).order_by('-latest_registration_no')
        else:
            queryset = qs.filter(user=request.user).annotate(
                
                latest_registration_no=Max('histories__registration_no')
            ).order_by('-latest_registration_no')
        return queryset


    



    

    class Media:
        js = ('assets/js/admin.js',)
        css = {
            'all': ('assets/css/admin.css',),
        }
    

@admin.register(History)
class HistoryAdmin(admin.ModelAdmin):
    
    #form = HistoryForm

    
    list_display = ('code','registration_no', 'patient_name', 'date_registered','date_of_exposure','muni_id', 'brgy_id','category_of_exposure', 
                    'exposure_type', 'source_of_exposure','status_of_animal', 'bite_site',
                    'immunization_status','washing_hands',)#
    
    #list_display_links = ['code',]
    search_fields = ['patient_id', 'source_of_exposure']
    list_filter = ('patient_id__user',BarangayFilter,MunicipalityFilter,)
    list_per_page = 10
    exclude = ('registration_no','washing_hands',)
    ordering = ('-registration_no',)

    #inlines = [HistoryInline, TreatmentInline] 

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        return form
 
    def patient_name(self, obj):
        return  f"{obj.patient_id.first_name} {obj.patient_id.last_name}"
    patient_name.short_description = 'Patient Name'

    """ def muni_name(self, obj):
        return obj.muni_id.muni_name
    muni_name.short_description = 'Municipality of Exposure' """

    """ def brgy_name(self, obj):
        return obj.brgy_id.brgy_name
    brgy_name.short_description = 'Barangay of Exposure' """
    
    def get_search_fields(self, request):
        return ['patient_id__first_name', 'patient_id__last_name']
    
    def get_list_display(self, request):
        if request.user.is_superuser:
            return self.list_display
        return ('registration_no', 'patient_name', 'date_registered','date_of_exposure','muni_id', 'brgy_id','category_of_exposure', 
                    'exposure_type', 'source_of_exposure','status_of_animal', 'bite_site',
                    'immunization_status','washing_hands',)#
    def get_list_filter(self, request):
        if request.user.is_superuser:
            return self.list_filter
        return (BarangayFilter, MunicipalityFilter)

    def get_readonly_fields(self, request, obj=None):
        if request.user.is_superuser:
            readonly_fields = [field.name for field in self.model._meta.fields if field.name != 'history_id']
            return readonly_fields
        return self.readonly_fields

    def has_add_permission(self, request):
        if request.user.is_superuser:
            return False
        return super().has_add_permission(request)

    def has_delete_permission(self, request, obj=None):
        if request.user.is_superuser:
            return False
        return super().has_delete_permission(request, obj)
    
    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return False
        return super().has_change_permission(request, obj)

    def save_model(self, request, obj, form, change):
        if request.user.is_superuser:
            return
        if not obj.pk:
            obj.patient_id.user = request.user
        super().save_model(request, obj, form, change)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(patient_id__user=request.user)
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'patient_id':
            if not request.user.is_superuser:
                kwargs['queryset'] = Patient.objects.filter(user=request.user)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    actions = ['']

    class Media:
        js = ('assets/js/admin.js',)
        css = {
            'all': ('assets/css/admin.css',),
        }

@admin.register(Treatment)    
class TreatmentAdmin(admin.ModelAdmin):
    list_display = ('code','registration_no', 'patient_name','category_of_exposure', 'vaccine_generic_name', 'vaccine_brand_name',
                    'vaccine_route','day0','day0_arrived', 'day3','day3_arrived', 'day7','day7_arrived', 
                    'day14','day28','rig_given', 'animal_alive','remarks')
                
    
    search_fields = ['patient_id',]
    list_per_page = 10
    list_filter = ['patient_id__user', 'vaccine_brand_name','vaccine_generic_name']
    #inlines = [HistoryInline,] 

    # Exclude the 'day0_arrived' field from the form
    exclude = ('day0_arrived', 'day3_arrived', 'day7_arrived','animal_alive',)


    def patient_name(self, obj):
        return  f"{obj.patient_id.first_name} {obj.patient_id.last_name}"
    patient_name.short_description = 'Patient Name'

    def get_search_fields(self, request):
        return ['patient_id__first_name', 'patient_id__last_name']
    

    def category_of_exposure(self, obj):
        return obj.get_category_of_exposure()
    category_of_exposure.short_description = 'Category of Exposure'
    
    def mark_day0(self, request, queryset):
        for treatment in queryset:
            treatment.day0_arrived = not treatment.day0_arrived
            treatment.save()
    mark_day0.short_description = "Day 0"

    def mark_day3(self, request, queryset):
        for treatment in queryset:
            treatment.day3_arrived = not treatment.day3_arrived
            treatment.save()
    mark_day3.short_description = "Day 3"

    def mark_day7(self, request, queryset):
        for treatment in queryset:
            treatment.day7_arrived = not treatment.day7_arrived
            treatment.save()
    mark_day7.short_description = "Day 7"

    def alive_animal(self,request,queryset):
        queryset.update(animal_alive=False)
    alive_animal.short_description = "Mark animal as dead"

    actions = ['mark_day0','mark_day3','mark_day7','alive_animal']

    
    
    def save_model(self, request, obj, form, change):
        if request.user.is_superuser:
            return  # Prevent saving for superusers
        if not obj.pk:
            obj.patient_id.user = request.user  # Ensure the patient is associated with the current user
        super().save_model(request, obj, form, change)
        
    def get_list_display(self, request):
        if request.user.is_superuser:
            return self.list_display
        return ('registration_no','patient_name','category_of_exposure', 'vaccine_generic_name', 'vaccine_brand_name',
                    'vaccine_route','day0','day0_arrived', 'day3','day3_arrived', 'day7','day7_arrived', 
                    'day14','day28','rig_given', 'animal_alive','remarks')

    def get_list_filter(self, request):
        if request.user.is_superuser:
            return self.list_filter
        return (BarangayFilter, MunicipalityFilter)
    
    def get_readonly_fields(self, request, obj=None):
        if request.user.is_superuser:
            readonly_fields = [field.name for field in self.model._meta.fields if field.name != 'treatment_id']
            return readonly_fields
        return self.readonly_fields
    
    def has_add_permission(self, request):
        if request.user.is_superuser:
            return False
        return super().has_add_permission(request)

    def has_delete_permission(self, request, obj=None):
        if request.user.is_superuser:
            return False
        return super().has_delete_permission(request, obj)
    
    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return False
        return super().has_change_permission(request, obj)
    
    def get_actions(self, request):
        actions = super().get_actions(request)
        if request.user.is_superuser:
            return {}  # Remove all actions for superusers
        return actions

    """ def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(patient_id__user=request.user) """
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        
        # Subquery to fetch the registration_no from the related History model
        history_subquery = History.objects.filter(
            patient_id=OuterRef('patient_id')
        ).order_by('-registration_no').values('registration_no')[:1]

        qs = qs.annotate(
            registration_no=Subquery(history_subquery)
        ).order_by('-registration_no')

        if request.user.is_superuser:
            return qs
        return qs.filter(patient_id__user=request.user)

    """ def get_queryset(self, request):
        qs = super().get_queryset(request)
        history_subquery = History.objects.filter(
            patient_id=OuterRef('patient_id')
        ).order_by('-registration_no').values('registration_no')[:1]
        
        if request.user.is_superuser:
            return qs.annotate(latest_registration_no=Subquery(history_subquery)).order_by('-latest_registration_no')
        else:
            return qs.filter(patient_id__user=request.user).annotate(latest_registration_no=Subquery(history_subquery)).order_by('-latest_registration_no') """




    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'patient_id':
            if not request.user.is_superuser:
                kwargs['queryset'] = Patient.objects.filter(user=request.user)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)



@admin.register(Barangay)
class BarangayAdmin(admin.ModelAdmin):
    list_display = ('brgy_name','muni_id')
    list_filter = ['brgy_name','muni_id__muni_name']
    list_per_page = 10
    #exclude = ('brgy_name',) 

    def muni_name(self, obj):
        return  f"{obj.muni_id.muni_name}"
    muni_name.short_description = 'Municipality Name'

    def get_search_fields(self, request):
        return ['muni_id__muni_name']

    class Media:
        js = ('assets/js/admin.js',)
        css = {
            'all': ('assets/css/admin.css',),
        }
        
@admin.register(Municipality)
class MunicipalityAdmin(admin.ModelAdmin):
    list_display = ['muni_name']
    

class LogEntryAdmin(admin.ModelAdmin):
    list_display = ('user',  'action_flag','object_repr', 'content_type','action_time', )
    list_filter = ('user', 'action_flag')
    search_fields = ('object_repr', 'change_message')
    list_per_page = 10

    def get_readonly_fields(self, request, obj=None):
        if request.user.is_superuser:
            readonly_fields = [field.name for field in self.model._meta.fields if field.name != 'treatment_id']
            return readonly_fields
        return self.readonly_fields
    
    def has_add_permission(self, request):
        if request.user.is_superuser:
            return False
        return super().has_add_permission(request)

    def has_delete_permission(self, request, obj=None):
        if request.user.is_superuser:
            return False
        return super().has_delete_permission(request, obj)
    
    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return False
        return super().has_change_permission(request, obj)

admin.site.register(LogEntry, LogEntryAdmin)





""" models = django.apps.apps.get_models()

for model in models:
    try:
        admin.site.register(model)
    except admin.sites.AlreadyRegistered:
        pass

admin.site.unregister(django.contrib.sessions.models.Session)
admin.site.unregister(django.contrib.contenttypes.models.ContentType)
admin.site.unregister(django.contrib.auth.models.Permission)  """

