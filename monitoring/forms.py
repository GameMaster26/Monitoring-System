from django import forms
from .models import Patient, History, Barangay
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from datetime import datetime,date,timedelta
from django.contrib.gis import forms as geoforms
from leaflet.forms.widgets import LeafletWidget



class CustomMapWidget(geoforms.OSMWidget):
    default_lon = 124.4642
    default_lat = 11.6400
    default_zoom = 12  # Adjust the zoom level as needed

class HistoryInlineForm(forms.ModelForm):
    class Meta:
        model = History
        fields = '__all__'
        widgets = {
            'geom': LeafletWidget(), 
        }



class HistoryForm(forms.ModelForm):
    class Meta:
        model = History
        fields = ['date_registered', 'date_of_exposure', 'muni_id', 'brgy_id', 'source_of_exposure',
                  'exposure_type', 'bite_site', 'provoked_status', 'immunization_status',
                  'status_of_animal', 'confinement_status', 'category_of_exposure', 'registration_no']


class PatientAdminForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Initially set Barangay queryset to all if no instance is being edited
        if self.instance.pk:
            initial_muni_id = self.instance.muni_id_id
            self.fields['brgy_id'].queryset = Barangay.objects.filter(muni_id=initial_muni_id)
        else:
            self.fields['brgy_id'].queryset = Barangay.objects.none()

        # If there is POST data (user has submitted the form), filter Barangays accordingly
        if 'muni_id' in self.data:
            try:
                muni_id = int(self.data.get('muni_id'))
                self.fields['brgy_id'].queryset = Barangay.objects.filter(muni_id=muni_id)
            except (ValueError, TypeError):
                pass  # fallback to empty queryset if invalid muni_id

