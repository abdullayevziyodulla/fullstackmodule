from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Doctor, Patient, Service
from .forms import *
from django.views.generic import ListView, UpdateView, CreateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin, PermissionRequiredMixin

# Create your views here.
def custom_permission_denied_view(request, exception=None):
    return render(request, '403.html', status=403)

# --- HOME PAGE ---
@login_required
def home(request):
    context={
        'patient_count': Patient.objects.count(),
        'doctor_count': Doctor.objects.count(),
        'service_count': Service.objects.count(),
        'appointment_count': Appointment.objects.count()
    }
    return render(request, 'home.html', context=context)


# --- LISTS PAGES ---
@permission_required("scheduling.view_patient", raise_exception=True)
def patients_list(request):
    # Query data
    patients = Patient.objects.all()
    # Create context
    context = {
        "patients": patients
    }
    # Pass context and render template
    return render(request, 'patients/patients.html', context)

@permission_required("scheduling.view_doctor", raise_exception=True)
def doctors_list(request):
    # Query data
    doctors = Doctor.objects.all()
    # Create context
    context = {
        "doctors": doctors
    }
    # Pass context and render template
    return render(request, 'doctors/doctors.html', context)

@permission_required("scheduling.view_service", raise_exception=True)
def services_list(request):
    # Query data
    services = Service.objects.all()
    # Create context
    context = {
        "services": services
    }
    # Pass context and render template
    return render(request, 'services/services.html', context)


# --- PATIENT CRUD ---
@permission_required("scheduling.add_patient", raise_exception=True)
def create_patient(request):
    if request.method == 'POST':
        form = PatientForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Patient was successfully added")
            return redirect('patients')
    else:
        form = PatientForm()
    
    return render(request, 'patients/create_patient.html', {'form': form})

@permission_required("scheduling.change_patient", raise_exception=True)
def update_patient(request, id):
    patient = get_object_or_404(Patient, id=id)
    form = PatientForm(request.POST or None, instance=patient)
    if form.is_valid():
        form.save()
        messages.info(request, "Patient successfully updated")
        return redirect('patients')
    return render(request, 'patients/update_patient.html', {'form': form})

@permission_required("scheduling.delete_patient", raise_exception=True)
def delete_patient(request, id):
    patient = get_object_or_404(Patient, id=id)
    if request.method == "POST":
        patient.delete()
        messages.warning(request, "Patient deleted")
        return redirect('patients')
    
    return render(request, 'patients/delete_patient.html', {'patient': patient})


# --- DOCTOR CRUD ---
@permission_required("scheduling.add_doctor", raise_exception=True)
def create_doctor(request):
    if request.method == 'POST':
        form = DoctorForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Doctor was successfully added")
            return redirect('doctors')
    else:
        form = DoctorForm()
    
    return render(request, 'doctors/create_doctor.html', {'form': form})

@permission_required("scheduling.change_doctor", raise_exception=True)
def update_doctor(request, id):
    doctor = get_object_or_404(Doctor, id=id)
    form = DoctorForm(request.POST or None, instance=doctor)
    if form.is_valid():
        form.save()
        messages.info(request, "Doctor successfully updated")
        return redirect('doctors')
    return render(request, 'doctors/update_doctor.html', {'form': form})

@permission_required("scheduling.delete_doctor", raise_exception=True)
def delete_doctor(request, id):
    doctor = get_object_or_404(Doctor, id=id)
    if request.method == "POST":
        doctor.delete()
        messages.warning(request, "Doctor deleted")
        return redirect('doctors')
    
    return render(request, 'doctors/delete_doctor.html', {'doctor': doctor})


# --- SERVICES CRUD ---
@permission_required("scheduling.add_service", raise_exception=True)
def create_service(request):
    if request.method == 'POST':
        form = ServiceForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "service was successfully added")
            return redirect('services')
    else:
        form = ServiceForm()
    
    return render(request, 'services/create_service.html', {'form': form})

@permission_required("scheduling.change_service", raise_exception=True)
def update_service(request, id):
    service = get_object_or_404(Service, id=id)
    form = ServiceForm(request.POST or None, instance=service)
    if form.is_valid():
        form.save()
        messages.info(request, "service successfully updated")
        return redirect('services')
    return render(request, 'services/update_service.html', {'form': form})

@permission_required("scheduling.delete_service", raise_exception=True)
def delete_service(request, id):
    service = get_object_or_404(service, id=id)
    if request.method == "POST":
        service.delete()
        messages.warning(request, "service deleted")
        return redirect('services')
    
    return render(request, 'services/delete_service.html', {'service': service})



# --- APPOINTMENT CRUD ---
@permission_required('scheduling.view_appointment', raise_exception=True)
def appointments_list(request):
    user = request.user

    if user.groups.filter(name__iexact='Doctor').exists():
        doctor_profile = getattr(user, 'doctor_profile', None)
        if doctor_profile:
            appointments = Appointment.objects.filter(doctor=doctor_profile, status__in=['pending', 'approved'], ).select_related('patient', 'service').order_by('-start_time')
        else:
            appointments = Appointment.objects.none()
    else:
        # Receptionists or admins
        appointments = Appointment.objects.select_related('doctor', 'patient', 'service').all().order_by('-start_time')

    return render(request, 'appointments/appointments.html', {'appointments': appointments})

@permission_required('scheduling.view_appointment', raise_exception=True)
def appointment_detail(request, pk):
    appointment = get_object_or_404(Appointment.objects.select_related('doctor', 'patient', 'service'), pk=pk)

    return render(request, 'appointments/detail.html', {
        'appointment': appointment,
    })

@permission_required('scheduling.add_appointment', raise_exception=True)
def create_appointment(request):
    from django.utils import timezone

    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            doctor = appointment.doctor
            start_time = appointment.start_time

            # Check overlapping appointments for the same doctor
            clash = Appointment.objects.filter(
                doctor=doctor,
                start_time__lte=start_time + timezone.timedelta(minutes=29),
                start_time__gte=start_time - timezone.timedelta(minutes=29)
            ).exists()

            if clash:
                messages.warning(request, f"Doctor {doctor.name} already has an appointment around {start_time:%Y-%m-%d %H:%M}.")
            else:
                appointment.save()
                messages.success(request, "Appointment created successfully.")
                return redirect('appointments')
    else:
        form = AppointmentForm()

    return render(request, 'appointments/create_appointment.html', {'form': form})


class AppointmentListView(PermissionRequiredMixin, ListView):
    model = Appointment
    template_name = 'appointments/appointments.html'
    context_object_name = 'appointments'
    ordering = ['-start_time']
    permission_required = ('scheduling.view_appointment')

class AppointmentCreateView(PermissionRequiredMixin, CreateView):
    model = Appointment
    form_class = AppointmentForm
    template_name = 'appointments/create_appointment.html'
    success_url = reverse_lazy('appointments')
    permission_required = ('scheduling.add_appointment')

class AppointmentUpdateView(PermissionRequiredMixin, UpdateView):
    model = Appointment
    form_class = AppointmentForm
    template_name = 'appointments/update_appointment.html'
    success_url = reverse_lazy('appointments')
    permission_required = ('scheduling.change_appointment')

class AppointmentDeleteView(PermissionRequiredMixin, DeleteView):
    model = Appointment
    template_name = 'appointments/delete_appointment.html'
    success_url = reverse_lazy('appointments')
    permission_required = ('scheduling.delete_appointment')    