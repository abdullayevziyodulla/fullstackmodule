from django.forms import ModelForm, DateInput
from .models import *
from django.core.exceptions import ValidationError

class DateInput(DateInput):
    input_type = 'date'

class BaseStyledModelForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            css = field.widget.attrs.get('class', '')
            field.widget.attrs['class'] = (css + ' form-control').strip()

class PatientForm(BaseStyledModelForm):
    class Meta:
        model = Patient
        fields = '__all__'
        widgets = {
            'dob': DateInput()
        }
        
    def clean_phone_number(self):
        phone = self.cleaned_data['phone_number']
        if not phone.startswith("998") or len(phone) != 12:
            raise ValidationError("Phone number must be in format: 998xxxxxxxxx")
        return phone
        
class DoctorForm(BaseStyledModelForm):
    class Meta:
        model = Doctor
        fields = '__all__'
        
    def clean_phone_number(self):
        phone = self.cleaned_data['phone_number']
        if not phone.startswith("998") or len(phone) != 12:
            raise ValidationError("Phone number must be in format: 998xxxxxxxxx")
        return phone
    
class ServiceForm(BaseStyledModelForm):
    class Meta:
        model = Service
        fields = '__all__'

class AppointmentForm(BaseStyledModelForm):
    class Meta:
        model = Appointment
        fields = '__all__'
        
        widgets = {
            'start_time': DateInput(attrs={
                'type': 'datetime-local',
                'class': 'form-control',
                'placeholder': 'Select date and time'
            })
        }