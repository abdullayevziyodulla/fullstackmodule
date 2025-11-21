from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter
from . import views_api

router = DefaultRouter()
router.register(r'patients', views_api.PatientViewSet)
router.register(r'doctors', views_api.DoctorViewSet)
router.register(r'services', views_api.ServiceViewSet)
router.register(r'appointments', views_api.AppointmentViewSet)

urlpatterns = [
    path('', views.home, name='home'),
    path('patients/', views.patients_list, name='patients'),
    path('doctors/', views.doctors_list, name='doctors'),
    path('services/', views.services_list, name='services'),
    # --- PATIENTS ---
    path('patients/create/', views.create_patient, name='create_patient'),
    path('patients/update/<int:id>', views.update_patient, name='update_patient'),
    path('patients/delete/<int:id>', views.delete_patient, name='delete_patient'),
    # --- DOCTORS ---
    path('doctors/create/', views.create_doctor, name='create_doctor'),
    path('doctors/update/<int:id>/', views.update_doctor, name='update_doctor'),
    path('doctors/delete/<int:id>/', views.delete_doctor, name='delete_doctor'),
    # ---SERVICES ---
    path('services/create/', views.create_service, name='create_service'),
    path('services/update/<int:id>/', views.update_service, name='update_service'),
    path('services/delete/<int:id>/', views.delete_service, name='delete_service'),
    # --- APPOINTMENTS ---
    path('appointments/', views.appointments_list, name='appointments'),
    path('appointment/<int:pk>', views.appointment_detail, name='appointment_detail'),
    path('appointments/create/', views.create_appointment, name='create_appointment'),
    path('appointments/update/<int:pk>', views.AppointmentUpdateView.as_view(), name='update_appointment'),
    path('appointments/delete/<int:pk>', views.AppointmentDeleteView.as_view(), name='delete_appointment'),
    # --- APIs ---
    path('api/', include(router.urls))
]

handler403 = "scheduling.views.custom_permission_denied_view"