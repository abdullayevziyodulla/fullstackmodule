from django.contrib import admin
from .models import *

# Register your models here.
@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('patient', 'doctor', 'service', 'start_time', 'status')
    search_fields = ('patient__name', 'service__name', 'doctor__name')
    list_filter = ('status', 'doctor', 'service', 'start_time')
    ordering = ('-start_time',)

class AppointmentInline(admin.TabularInline):
    model = Appointment
    extra = 1

@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ('name', 'specialization')
    search_fields = ('name', 'specialization')
    list_filter = ('specialization',)
    inlines = [AppointmentInline]

@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ('name', 'dob')
    search_fields = ('name', 'dob')
    list_filter = ('dob',)
    inlines = [AppointmentInline]

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    inlines = [AppointmentInline]