from .models import Patient,History,Treatment,Municipality,Barangay,UserMessage
from django.contrib.contenttypes.admin import GenericTabularInline,GenericInlineModelAdmin,GenericInlineModelAdminChecks,GenericStackedInline
from django.contrib.auth.models import Group, User,Permission
from django.contrib.admin.models import LogEntry
from django.contrib.sessions.models import Session
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.admin import UserAdmin,GroupAdmin
from django.contrib.admin import AdminSite
from django.contrib.gis import admin
from django.contrib.gis.admin import GISModelAdmin
from django.contrib.gis.db import models as geomodels
from django.contrib.admin import SimpleListFilter
from django.db.models import Max,Q,OuterRef, Subquery
from django.utils.safestring import mark_safe
from django.urls import path
from django.http import HttpResponseRedirect
from django.urls import reverse
from django import forms
from leaflet.admin import LeafletGeoAdmin
from leaflet.forms.widgets import LeafletWidget
from datetime import datetime,timedelta
from .forms import PatientAdminForm,HistoryForm,HistoryInlineForm,CustomMapWidget,MessageUserForm
from django.urls import path
from django.shortcuts import render, redirect
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html
from django.contrib import messages
from django.contrib.auth import get_user_model

# Custom User Admin class
""" class CustomUserAdmin(admin.ModelAdmin):
    list_display = ("username", "first_name", "last_name", "email", "send_message_link")

    # Define additional URL paths for sending messages
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('<int:user_id>/send_message/', self.send_message_view, name="send_message_user"),
        ]
        return custom_urls + urls

    # Method to generate a clickable "Send Message" link in the user list
    def send_message_link(self, obj):
        return format_html(
            '<a class="button" href="{}">Send Message</a>',
            reverse("admin:send_message_user", args=[obj.pk])
        )
    send_message_link.short_description = 'Message'

    # The view to handle sending a message to the user
    def send_message_view(self, request, user_id):
        user = get_user_model().objects.get(id=user_id)  # Retrieve the user by ID

        if request.method == 'POST':
            form = MessageUserForm(request.POST)
            if form.is_valid():
                form.send_message(user)  # Save the message to the database
                messages.success(request, f"Message sent to {user.get_full_name()}.")
                return redirect('admin:auth_user_change', user_id)
        else:
            form = MessageUserForm()

        return render(
            request,
            'admin/send_message.html',  # Make sure this template exists
            {
                'form': form,
                'user': user,
            }
        )

# Unregister the default UserAdmin to prevent conflicts
admin.site.unregister(get_user_model())

# Register the custom UserAdmin
admin.site.register(get_user_model(), CustomUserAdmin) """


""" @admin.register(UserMessage)
class UserMessageAdmin(admin.ModelAdmin):
    list_display = ('user', 'subject', 'sent_at') """

class CustomGeoAdmin(LeafletGeoAdmin):
    
    class Media:
        # Include your custom CSS file here
        css = {
            'all': ('assets/css/muni.css',),  
        }
        js = ('assets/js/reset_view.js',
            'assets/js/municipality_center.js',
            'https://code.jquery.com/jquery-3.6.0.min.js',  # Include jQuery if not already included
            'assets/js/mapHistory.js',   
        )

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
    form = HistoryInlineForm
    extra = 0

    def get_fields(self, request, obj=None):
        fields = ['date_registered', 'date_of_exposure', 'muni_id', 'brgy_id','source_of_exposure','category_of_exposure', 
                    'exposure_type','bite_site', 'provoked_status', 'immunization_status',
                    'status_of_animal', 'confinement_status',  'washing_hands', 'human_rabies',]#'geom'
                  
        # Always add 'registration_no' if viewing an existing object
        if obj:
            fields.insert(0, 'registration_no')
        return fields

    def get_formset(self, request, obj=None, **kwargs):
        formset = super().get_formset(request, obj, **kwargs)
        # If editing an existing object, control the behavior of 'registration_no'
        if obj:
            if request.user.is_superuser and 'registration_no' in formset.form.base_fields:
                # Set 'registration_no' as read-only and not required for superusers
                formset.form.base_fields['registration_no'].widget.attrs['readonly'] = True
                formset.form.base_fields['registration_no'].required = False
        else:
            # For a new object, ensure 'registration_no' is removed
            formset.form.base_fields.pop('registration_no', None)
        return formset

    def get_readonly_fields(self, request, obj=None):
        readonly_fields = []
        if obj and request.user.is_superuser:
            readonly_fields = [field.name for field in self.model._meta.fields if field.name != 'id']
        return readonly_fields

class TreatmentInline(admin.StackedInline):
    model = Treatment
    extra = 0


class AgeFilter(SimpleListFilter):
    title = 'Age'  #Name for the filter
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

class BarangayFilter(SimpleListFilter):
    title = 'Barangay'
    parameter_name = 'brgy_id'
    
    def lookups(self, request, model_admin):
        # Retrieve distinct barangay names from the Patient model
        return Patient.objects.values_list('brgy_id__brgy_name', 'brgy_id__brgy_name').distinct()

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(brgy_id__brgy_name=self.value())

class MunicipalityFilter(SimpleListFilter):
    title = 'Municipality'
    parameter_name = 'muni_id'

    def lookups(self, request, model_admin):
        # Retrieve distinct municipality names from the Patient model
        return Patient.objects.values_list('muni_id__muni_name', 'muni_id__muni_name').distinct()

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(muni_id__muni_name=self.value())

@admin.register(Patient)
class PatientAdmin(LeafletGeoAdmin):
    list_display = ('code', 'first_name','middle_name', 'last_name', 'muni_id','brgy_id', 'age', 'sex','contactNumber', )
    list_per_page = 10
    
    search_fields = ['first_name','middle_name','last_name','muni_id__muni_name','brgy_id__brgy_name','sex__iexact']
    list_filter = ('user__code', AgeFilter,'muni_id', 'brgy_id', 'sex')
    inlines = [HistoryInline, TreatmentInline] 
    exclude = ('user',) 
    ordering = ('-patient_id',)


    """ def get_search_results(self, request, queryset, search_term):
        # Allow search across all patients for all users, also show user code during search
        if search_term:
            queryset = Patient.objects.filter(
                Q(first_name__icontains=search_term) |
                Q(middle_name__icontains=search_term) |
                Q(last_name__icontains=search_term)
            ).select_related('user')  
        return queryset, False   """

    """ def get_list_display(self, request):
        # If not searching or for regular users, remove 'code' from the list view
        if not request.GET.get('q'):  # When no search query
            if request.user.is_superuser:
                return ('code', 'first_name', 'middle_name', 'last_name', 'muni_id', 'brgy_id', 'age', 'sex', 'contactNumber')
            else:
                return ('first_name', 'middle_name', 'last_name', 'muni_id', 'brgy_id', 'age', 'sex', 'contactNumber')
        else:  # When search query is present
            return ('code', 'first_name', 'middle_name', 'last_name', 'muni_id', 'brgy_id', 'age', 'sex', 'contactNumber') """
    
    def get_list_display(self, request):
        if request.user.is_superuser:
            return ('code', 'first_name', 'middle_name', 'last_name', 'muni_id', 'brgy_id', 'age', 'sex', 'contactNumber')
        else:
            return ('first_name', 'middle_name', 'last_name', 'muni_id', 'brgy_id', 'age', 'sex', 'contactNumber')

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

    # Allow editing patients by ensuring the correct patient object is retrieved
    def get_object(self, request, object_id, from_field=None):
        try:
            # Get the patient by its ID, bypassing user-based filtering for editing
            return Patient.objects.get(pk=object_id)
        except Patient.DoesNotExist:
            return None  # Return None if the patient doesn't exist

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
        if request.user.is_superuser and request.user.is_staff:
            return False
        """ return super().has_delete_permission(request, obj) """
    
    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser and request.user.is_staff:
            return False
        """ return super().has_change_permission(request,obj) """
    
    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.user = request.user
        super().save_model(request, obj, form, change)

    def each_context(self, request):
        context = super().each_context(request)
        context['search_name'] = '<script src="/static/placeholder/search_name.js"></script>'
        return context

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


    def get_list_filter(self, request):
        if request.user.is_superuser:
            return self.list_filter
        return (AgeFilter, 'muni_id', 'brgy_id')


    class Media:
        js = ('assets/js/admin.js',)
        css = {
            'all': ('assets/css/admin.css',),
        }
    

@admin.register(History)
class HistoryAdmin(CustomGeoAdmin):
    
    #form = HistoryForm    
    list_display = ('code','registration_no', 'patient_name', 'date_registered','date_of_exposure','muni_id', 'brgy_id','category_of_exposure', 
                    'exposure_type', 'source_of_exposure','status_of_animal', 'bite_site',
                    'immunization_status','washing_hands', 'human_rabies')#'get_latitude', 'get_longitude'
    #list_display_links = ['code',]
    search_fields = [
        'registration_no', 'patient_id__first_name','patient_id__last_name','date_registered', 'date_of_exposure',
        'muni_id__muni_name','brgy_id__brgy_name','category_of_exposure','source_of_exposure','exposure_type',
        'bite_site','provoked_status','immunization_status__iexact','status_of_animal','confinement_status',
    ]
    # Define the field order in the form
    fields = (
        'patient_id', 'registration_no', 'date_registered', 'date_of_exposure', 'muni_id', 'brgy_id',
        'category_of_exposure', 'source_of_exposure', 'exposure_type', 'bite_site', 'provoked_status',
        'immunization_status', 'status_of_animal', 'confinement_status','washing_hands', 'human_rabies', 'latitude', 'longitude', 'geom'
    )#, 'latitude', 'longitude', 'geom'

    list_filter = ('patient_id__user__code','muni_id', 'brgy_id','category_of_exposure',)
    list_per_page = 10
    """ exclude = ('washing_hands',) """
    ordering = ('-patient_id',)

    #inlines = [HistoryInline, TreatmentInline]
    
    def get_latitude(self, obj):
        return obj.latitude

    get_latitude.short_description = 'Latitude'

    def get_longitude(self, obj):
        return obj.longitude

    get_longitude.short_description = 'Longitude'

    """ def get_search_results(self, request, queryset, search_term):
        if search_term:
            queryset = queryset.filter(
                Q(patient_id__first_name__icontains=search_term) |
                Q(patient_id__middle_name__icontains=search_term) |
                Q(patient_id__last_name__icontains=search_term)
            ).select_related('patient_id') 
        return queryset, False   """

    """ def get_list_display(self, request):
        if not request.GET.get('q'):  # When no search query
            if request.user.is_superuser:
                return ('code','registration_no', 'patient_name', 'date_registered','date_of_exposure','muni_id', 'brgy_id','category_of_exposure', 
                    'exposure_type', 'source_of_exposure','status_of_animal', 'bite_site',
                    'immunization_status','washing_hands', 'human_rabies')
            else:
                return ('registration_no', 'patient_name', 'date_registered','date_of_exposure','muni_id', 'brgy_id','category_of_exposure', 
                    'exposure_type', 'source_of_exposure','status_of_animal', 'bite_site',
                    'immunization_status','washing_hands', 'human_rabies')
        else:  # When search query is present
            return ('code','registration_no', 'patient_name', 'date_registered','date_of_exposure','muni_id', 'brgy_id','category_of_exposure', 
                    'exposure_type', 'source_of_exposure','status_of_animal', 'bite_site',
                    'immunization_status','washing_hands', 'human_rabies') """
    
    def get_list_display(self, request):
        if request.user.is_superuser:
            return ('code','registration_no', 'patient_name', 'date_registered','date_of_exposure','muni_id', 'brgy_id','category_of_exposure', 
                'exposure_type', 'source_of_exposure','status_of_animal', 'bite_site',
                'immunization_status','washing_hands', 'human_rabies')
        else:
            return ('registration_no', 'patient_name', 'date_registered','date_of_exposure','muni_id', 'brgy_id','category_of_exposure', 
                'exposure_type', 'source_of_exposure','status_of_animal', 'bite_site',
                'immunization_status','washing_hands', 'human_rabies')

    # Modify the queryset to limit data visibility based on user
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs  # Superusers can see all records
        else:
            return qs.filter(patient_id__user=request.user)  # Regular users only see their own records
    
    def get_search_results(self, request, queryset, search_term):
        
        queryset, use_distinct = super().get_search_results(request, queryset, search_term)

        # Split the search term into individual parts for better flexibility
        search_terms = search_term.split()

        # Perform a case-insensitive search (icontains) across the patient names (first, middle, last)
        for term in search_terms:
            queryset = queryset.filter(
                Q(patient_id__first_name__icontains=term) |
                Q(patient_id__middle_name__icontains=term) |
                Q(patient_id__last_name__icontains=term)
            )

        # If the user is not a superuser, filter the results to only show their own data
        if not request.user.is_superuser:
            queryset = queryset.filter(patient_id__user=request.user)

        return queryset, use_distinct

    """ def get_search_results(self, request, queryset, search_term):
        queryset, use_distinct = super().get_search_results(request, queryset, search_term)
        if not request.user.is_superuser:
            # Regular users can only search within their own data
            queryset = queryset.filter(patient_id__user=request.user)
        return queryset, use_distinct """
        
    """ def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs     
        # If not searching, filter by the current user (for regular users)
        if not request.GET.get('q'):  # No search query
            return qs.filter(patient_id__user=request.user)       
        # Otherwise, show all records even if the user is not the owner (search case)
        return qs """

    def get_fields(self, request, obj=None):
        fields = super().get_fields(request, obj)
        if obj is None:  # If adding a new object, remove 'registration_no'
            fields = [field for field in fields if field != 'registration_no']
        return fields
 
    def patient_name(self, obj):
        return  f"{obj.patient_id.first_name} {obj.patient_id.last_name}"
    patient_name.short_description = 'Patient Name'

    
    def get_list_filter(self, request):
        if request.user.is_superuser:
            return self.list_filter
        return ('muni_id', 'brgy_id','category_of_exposure',)

    def get_readonly_fields(self, request, obj=None):
        # For superuser, make all fields readonly except 'geom'
        if request.user.is_superuser:
            # Exclude both 'geom' and 'history_id' from readonly fields
            readonly_fields = [field.name for field in self.model._meta.fields if field.name != 'geom']
            return readonly_fields
        return self.readonly_fields
    
    def has_add_permission(self, request):
        if request.user.is_superuser:
            return False
        return super().has_add_permission(request)

    def has_delete_permission(self, request, obj=None):
        if request.user.is_superuser and request.user.is_staff:
            return False
        """ return super().has_delete_permission(request, obj) """
    
    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser and request.user.is_staff:
            return False
        """ return super().has_change_permission(request, obj) """

    def save_model(self, request, obj, form, change):
        if request.user.is_superuser:
            return
        if not obj.pk:
            obj.patient_id.user = request.user
        super().save_model(request, obj, form, change)
        
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'patient_id':
            if not request.user.is_superuser:
                kwargs['queryset'] = Patient.objects.filter(user=request.user)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    actions = ['']

    """ class Media:
        js = (
            'https://cdn.jsdelivr.net/npm/leaflet@1.9.4/dist/leaflet.js',
            'assets/js/admin_geom.js',  # Your custom script
        )
        css = {
            'all': ('https://cdn.jsdelivr.net/npm/leaflet@1.9.4/dist/leaflet.css',) 
        }
 """
@admin.register(Treatment)    
class TreatmentAdmin(admin.ModelAdmin):
    list_display = ('code','registration_no', 'patient_name','category_of_exposure', 'vaccine_generic_name', 'vaccine_brand_name',
                    'vaccine_route', 'day0','day0_arrived', 'day3','day3_arrived', 'day7','day7_arrived', 
                    'day14','day28','tcv_given','booster1','booster2','hrig_given', 'rig_given', 'animal_alive','remarks')
                
    search_fields = ['patient_id__first_name','patient_id__last_name','vaccine_route__iexact']
    list_per_page = 10
    list_filter = ['patient_id__user__code','patient_id__histories__category_of_exposure', 'vaccine_brand_name','vaccine_generic_name']
    #inlines = [HistoryInline,] 

    # Exclude the 'day0_arrived' field from the form
    exclude = ('day0_arrived', 'day3_arrived', 'day7_arrived','day28_arrived',)
    ordering = ('-patient_id',)

    def get_search_results(self, request, queryset, search_term):
        # Allow search across all patients for all users, also show user code during search
        if search_term:
            queryset = queryset.filter(
                Q(patient_id__first_name__icontains=search_term) |
                Q(patient_id__middle_name__icontains=search_term) |
                Q(patient_id__last_name__icontains=search_term)
            ).select_related('patient_id')  # Pre-fetch user data, including the user code
        return queryset, False  # Return the modified queryset

    def get_list_display(self, request):
        
        # If not searching or for regular users, remove 'code' from the list view
        if not request.GET.get('q'):  # When no search query
            if request.user.is_superuser:
                return ('code','registration_no', 'patient_name','category_of_exposure', 'vaccine_generic_name', 'vaccine_brand_name',
                    'vaccine_route', 'day0','day0_arrived', 'day3','day3_arrived', 'day7','day7_arrived', 
                    'day14','day28','tcv_given','booster1','booster2','hrig_given', 'rig_given', 'animal_alive','remarks')
            else:
                return ('registration_no', 'patient_name','category_of_exposure', 'vaccine_generic_name', 'vaccine_brand_name',
                    'vaccine_route', 'day0','day0_arrived', 'day3','day3_arrived', 'day7','day7_arrived', 
                    'day14','day28','tcv_given','booster1','booster2','hrig_given', 'rig_given', 'animal_alive','remarks')
        else:  # When search query is present
            return ('code','registration_no', 'patient_name','category_of_exposure', 'vaccine_generic_name', 'vaccine_brand_name',
                    'vaccine_route', 'day0','day0_arrived', 'day3','day3_arrived', 'day7','day7_arrived', 
                    'day14','day28','tcv_given','booster1','booster2','hrig_given', 'rig_given', 'animal_alive','remarks')

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        
        # If user is superuser, show all records
        if request.user.is_superuser:
            return qs     
        # If not searching, filter by the current user (for regular users)
        if not request.GET.get('q'):  # No search query
            return qs.filter(patient_id__user=request.user)       
        # Otherwise, show all records even if the user is not the owner (search case)
        return qs

    def patient_name(self, obj):
        return  f"{obj.patient_id.first_name} {obj.patient_id.last_name}"
    patient_name.short_description = 'Patient Name'

    def get_search_fields(self, request):
        return ['patient_id__first_name', 'patient_id__last_name']
    
    """ def registration_no(self, obj):
        return obj.registration_no()
    registration_no.short_description = 'Registration Number' """

    def category_of_exposure(self, obj):
        return obj.get_category_of_exposure()
    category_of_exposure.short_description = 'Exposure Category'
    
    def save_model(self, request, obj, form, change):
        if request.user.is_superuser:
            return  
        if not obj.pk:
            obj.patient_id.user = request.user
        super().save_model(request, obj, form, change)

    def get_list_filter(self, request):
        if request.user.is_superuser:
            return self.list_filter
        return ('patient_id__histories__category_of_exposure','rig_given', 'vaccine_brand_name','vaccine_generic_name')
    
    def get_readonly_fields(self, request, obj=None):
        if request.user.is_superuser:
            readonly_fields = [field.name for field in self.model._meta.fields if field.name != 'treatment_id']
            return readonly_fields
        return self.readonly_fields
    
    def has_add_permission(self, request):
        if request.user.is_superuser:
            return False
        return super().has_add_permission(request)
    
    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser and request.user.is_staff:
            return False
        """ return super().has_change_permission(request, obj) """

    def has_delete_permission(self, request, obj=None):
        if request.user.is_superuser and request.user.is_staff:
            return False
        """ return super().has_delete_permission(request, obj) """
    
    def get_actions(self, request):
        actions = super().get_actions(request)
        if request.user.is_superuser:
            return {}  
        return actions

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'patient_id':
            if not request.user.is_superuser:
                kwargs['queryset'] = Patient.objects.filter(user=request.user)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)\
    
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

    def mark_day28(self, request, queryset):
        for treatment in queryset:
            treatment.day28_arrived = not treatment.day28_arrived
            treatment.save()
    mark_day28.short_description = "Day 28"

    def mark_as_animal(self,request,queryset):
        for treatment in queryset:
            treatment.animal_alive = not treatment.animal_alive
            treatment.save()
    mark_as_animal.short_description = "Animal is Dead"

    actions = ['mark_day0','mark_day3','mark_day7','mark_day28', 'mark_as_animal',]



@admin.register(Barangay)
class BarangayAdmin(CustomGeoAdmin):
    list_display = ('brgy_name','muni_id',)#'tmp_muni'
    list_filter = ['brgy_name','muni_id']
    #search_fields = ['brgy_name','muni_id']
    list_per_page = 10
    #exclude = ('brgy_name',) 

    def muni_name(self, obj):
        return  f"{obj.muni_id.muni_name}"
    muni_name.short_description = 'Municipality Name'

    def get_search_fields(self, request):
        return ['muni_id__muni_name','brgy_name']

    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser and request.user.is_staff:
            return False
        """ return super().has_change_permission(request, obj) """
    
    def has_delete_permission(self, request, obj=None):
        return not request.user.is_superuser

    class Media:
        js = ('assets/js/admin.js',)
        css = {
            'all': ('assets/css/admin.css',),
        }
        
@admin.register(Municipality)
class MunicipalityAdmin(CustomGeoAdmin):
    list_display = ('muni_name',)#'latitude', 'longitude'
    fields = ('muni_name','geom',)

    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser and request.user.is_staff:
            return False
        """ return super().has_change_permission(request, obj) """

    def has_delete_permission(self, request, obj=None):
        return not request.user.is_superuser

class LogEntryAdmin(admin.ModelAdmin):
    list_display = ('user', 'action_flag','object_repr', 'content_type','action_time', )
    fields = ('user', 'action_flag','object_repr', 'content_type','action_time',)
    list_filter = ('user__code', 'action_flag')
    search_fields = ('object_repr', 'change_message','user','action_flag')
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

    """ def has_delete_permission(self, request, obj=None):
        if request.user.is_superuser:
            return False
        return super().has_delete_permission(request, obj) """
    
    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return False
        return super().has_change_permission(request, obj)

admin.site.register(LogEntry, LogEntryAdmin)

# Override UserAdmin
class CustomUserAdmin(UserAdmin):
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        # Filter out session and contenttypes permissions
        if 'user_permissions' in form.base_fields:
            content_type_ids = ContentType.objects.filter(
                model__in=['session', 'contenttype']
            ).values_list('id', flat=True)

            form.base_fields['user_permissions'].queryset = Permission.objects.exclude(content_type_id__in=content_type_ids)
        return form

# Override GroupAdmin
class CustomGroupAdmin(GroupAdmin):
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        # Filter out session and contenttypes permissions
        if 'permissions' in form.base_fields:
            content_type_ids = ContentType.objects.filter(
                model__in=['session', 'contenttype']
            ).values_list('id', flat=True)

            form.base_fields['permissions'].queryset = Permission.objects.exclude(content_type_id__in=content_type_ids)
        return form

# Re-register the UserAdmin and GroupAdmin
admin.site.unregister(User)
admin.site.unregister(Group)
admin.site.register(User, CustomUserAdmin)
admin.site.register(Group, CustomGroupAdmin)


""" admin.site.register(Session)
admin.site.register(ContentType)
admin.site.register(Permission) """



