from django import forms
from .models import Patient, History, Barangay,UserMessage
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from datetime import datetime,date,timedelta
from django.contrib.gis import forms as geoforms
from leaflet.forms.widgets import LeafletWidget
from django.core.mail import send_mail
from django.contrib.auth import get_user_model

class MessageUserForm(forms.Form):
    subject = forms.CharField(max_length=100, label="Subject")
    message = forms.CharField(widget=forms.Textarea, label="Message")

    def send_message(self, user):
        subject = self.cleaned_data['subject']
        message = self.cleaned_data['message']
        
        # Save the message to the database
        UserMessage.objects.create(user=user, subject=subject, message=message)



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

class PatientSearch(forms.ModelForm):
    class Meta:
        model = Patient
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        # Extract the user from the kwargs
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        # Make fields readonly if the user does not own the data
        if self.user and self.instance and self.instance.user != self.user:
            for field in self.fields:
                self.fields[field].widget.attrs['readonly'] = True
                self.fields[field].disabled = True

