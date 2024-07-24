from django import forms
from .models import Patient, History, Barangay
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from datetime import datetime,date,timedelta

class HistoryForm(forms.ModelForm):
    class Meta:
        model = History
        fields = '__all__'

    class Media:
        js = ('assets/js/source.js',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['other_animal'].required = False  # Gawing hindi required by default

        if 'source_of_exposure' in self.data:
            source_of_exposure = self.data['source_of_exposure']
        else:
            source_of_exposure = self.instance.source_of_exposure if self.instance.pk else None

        if source_of_exposure == 'Others':
            self.fields['other_animal'].required = True
        else:
            self.fields['other_animal'].required = False
            self.fields['other_animal'].widget.attrs['style'] = 'display:none'


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


class HistoryAdminForm(forms.ModelForm):
    class Meta:
        model = History
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['brgy_id'].queryset = Barangay.objects.none()  # Initially set to empty queryset

        if 'muni_id' in self.data:
            try:
                muni_id = int(self.data.get('muni_id'))
                self.fields['brgy_id'].queryset = Barangay.objects.filter(muni_id=muni_id)
            except (ValueError, TypeError):
                pass  # fallback to empty queryset if invalid muni_id
        elif self.instance.pk:
            self.fields['brgy_id'].queryset = self.instance.muni_id.barangays.all()


""" class HistoryForm(forms.ModelForm):
    class Meta:
        model = History
        exclude = ['registration_no ']

    def __init__(self, *args, **kwargs):
        super(HistoryForm, self).__init__(*args, **kwargs)
        if not self.instance.pk:  # Only prefill for new objects
            self.fields['registration_no'].initial = self.generate_registration_no()

    def generate_registration_no(self):
        current_year = date.today().year
        last_history = History.objects.filter(
            registration_no__startswith=f'{current_year}-'
        ).order_by('registration_no').last()

        if last_history:
            last_reg_no = last_history.registration_no
            last_reg_num = int(last_reg_no.split('-')[-1])
            new_reg_num = last_reg_num + 1
        else:
            new_reg_num = 1

        new_registration_no = f'{current_year}-{new_reg_num:05d}'
        return new_registration_no """

class HistoryInlineForm(forms.ModelForm):
    class Meta:
        model = History
        fields = '__all__'

    """ def save(self, commit=True):
        instance = super(HistoryInlineForm, self).save(commit=False)
        if not instance.registration_no:  # Only set the registration number if it's not already set
            instance.registration_no = instance.generate_registration_no()
        if commit:
            instance.save()
        return instance """
    
   
    def __init__(self, *args, **kwargs):
        super(HistoryInlineForm, self).__init__(*args, **kwargs)
        if not self.instance.pk:  # Only prefill for new objects
            self.fields['registration_no'].initial = self.generate_registration_no()

    def generate_registration_no(self):
        current_year = date.today().year
        last_history = History.objects.filter(
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