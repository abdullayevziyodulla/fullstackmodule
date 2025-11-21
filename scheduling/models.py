from django.db.models import (
    OneToOneField,
    Model, CharField, EmailField, DateField, TextField, TextChoices, DateTimeField,
    ForeignKey, CASCADE)
from django.contrib.auth.models import User

# Create your models here.
class Doctor(Model):
    name = CharField(max_length=100)
    email = EmailField(unique=True)
    specialization = CharField(max_length=100)
    phone_number = CharField(max_length=15)
    user = OneToOneField(User, on_delete=CASCADE, null=True, blank=True, related_name='doctor_profile')

    def __str__(self):
        return f'{self.name} - {self.specialization}'

class Patient(Model):
    name = CharField(max_length=100)
    email = EmailField(unique=True)
    dob = DateField()
    phone_number = CharField(max_length=15)

    def __str__(self):
        return f'{self.name} - {self.dob}'

class Service(Model):
    name = CharField(max_length=100)
    description = TextField(blank=True)
    
    def __str__(self):
        return self.name

class Appointment(Model):
    class Status(TextChoices):
        PENDING = "pending", "Pending"
        APPROVED = "approved", "Approved"
        CANCELLED = "cancelled", "Cancelled"
    
    patient = ForeignKey('Patient', on_delete=CASCADE, related_name='appointments')
    doctor = ForeignKey('Doctor', on_delete=CASCADE, related_name='appointment')
    service = ForeignKey('Service', on_delete=CASCADE, related_name='appointments')
    
    start_time = DateTimeField()
    status = CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    notes = TextField(blank=True)
    
    class Meta:
        ordering = ['start_time']
    
    def __str__(self):
        return f'{self.patient} -> {self.doctor} @ {self.start_time:%Y-%m-%d %H:%M}'