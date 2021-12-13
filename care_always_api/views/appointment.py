from django.core.exceptions import ValidationError
from rest_framework import status
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from care_always_api.models import Appointment, Provider
from django.contrib.auth.models import User
from rest_framework.decorators import action

class AppointmentView(ViewSet):
    def list(self, request):
        current_user = request.auth.user

        # filter appointments here
        appointments = Appointment.objects.all()
        if appointments is not None:
            current_user_appointments = appointments.filter(user_id=current_user)
        
        
        serializer = AppointmentSerializer(
            current_user_appointments, many=True, context={'request': request})
        return Response(serializer.data)
    
    def retrieve(self, request, pk=None):
        try:
            appointment = Appointment.objects.get(pk=pk)
            serializer = AppointmentSerializer (appointment, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)
    
    def create(self, request):

        try:
            appointment = Appointment.objects.create(
                date=request.data["date"],
                time=request.data["time"],
                provider=Provider.objects.get(pk=request.data["providerId"]),
                user=request.auth.user
            )
            serializer = AppointmentSerializer(appointment, context={'request': request})
            return Response(serializer.data)
        
        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)
    
    def destroy(self, request, pk=None):

        try:
            appointment = Appointment.objects.get(pk=pk)
            appointment.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)
        
        except Appointment.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class AppointmentUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'email', 'username', 'password')

class AppointmentSerializer(serializers.ModelSerializer):
    user = AppointmentUserSerializer()
    class Meta:
        model = Appointment
        fields = ('id', 'date', 'time', 'provider', 'user')
        depth = 1