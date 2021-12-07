from django.core.exceptions import ValidationError
from rest_framework import status
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from care_always_api.models import Appointment, Provider, Question
from django.contrib.auth.models import User
from rest_framework.decorators import action

class AppointmentView(ViewSet):
    def list(self, request):
        user = User.objects.get(user=request.auth.user)
        appointments = Appointment.objects.all()

        for appointment in appointments:
            appointment.scheduled = user in appointment.attendees.all()
        
        serializer = AppointmentSerializer(
            appointments, many=True, context={'request': request})
        return Response(serializer.data)
    
    def retrieve(self, request, pk=None):
        try:
            appointment = Appointment.objects.get(pk=pk)
            serializer = AppointmentSerializer (appointment, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)
    
    def create(self, request):
        user = User.objects.get(user=request.auth.user)
        appointment=Appointment.objects.get(pk=request.data["appointmentId"])

        try:
            appointment = Appointment.objects.create(
                date=request.data["date"],
                time=request.data["time"],
                provider=Provider.objects.get(pk=request.data["providerId"]),
                user=user,
                question=Question.objects.get(pk=request.data["questionId"])
            )
            serializer = AppointmentSerializer(appointment, context={'request': request})
            return Response(serializer.data)
        
        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)