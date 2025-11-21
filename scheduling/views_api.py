from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import *
from .serializers import *
from datetime import timedelta

class PatientViewSet(viewsets.ModelViewSet):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer

class DoctorViewSet(viewsets.ModelViewSet):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer

class ServiceViewSet(viewsets.ModelViewSet):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer

class AppointmentViewSet(viewsets.ModelViewSet):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        doctor = serializer.validated_data['doctor']
        start_time = serializer.validated_data['start_time']
        
        clashes = Appointment.objects.filter(
            doctor=doctor, 
            start_time__lte=start_time + timedelta(minutes=29),
            start_time__gte=start_time - timedelta(minutes=29)
        ).exists()
        
        if clashes:
            return Response({'detail': "Doctor already has an appointment during this time slot"}, status=status.HTTP_400_BAD_REQUEST)
        
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)