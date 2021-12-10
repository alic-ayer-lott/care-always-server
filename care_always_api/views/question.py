from django.core.exceptions import ValidationError
from django.views.generic.base import View
from rest_framework import status
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from care_always_api.models import Question
from django.contrib.auth.models import User
from rest_framework.decorators import action

from care_always_api.models.appointment import Appointment

class QuestionView(ViewSet):

    def list(self, request):

        questions = Question.objects.all()

        serializer = QuestionSerializer(
            questions, many=True, context={'request': request})
        return Response(serializer.data)

    def retrieve(self, request, pk=None):

        try:
            question = Question.objects.get(pk=pk)
            serializer = QuestionSerializer(question, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)
    
    def create(self, request):
        appointment = Appointment.objects.get(pk=request.data["appointmentId"])

        try:
            question = Question.objects.create(
                content=request.data["content"],
                appointment=appointment
            )
            serializer = QuestionSerializer(question, context={'request': request})
            return Response(serializer.data)
        
        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)
    
    def update(self, request, pk=None):

        question = Question.objects.get(pk=pk)
        question.content = request.data["content"]

        question.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)
    
    def destroy(self, request, pk=None):

        try:
            question = Question.objects.get(pk=pk)
            question.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)
        
        except Question.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
        
        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class QuestionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Question
        fields = ('id', 'content')
        depth = 1