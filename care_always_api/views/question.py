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

class QuestionView(ViewSet):

    def list(self, request):

        questions = Question.objects.all()

        serializer = QuestionSerializer(
            questions, many=True, context={'request': request})
        return Response(serializer.data)


class QuestionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Question
        fields = ('id', 'content')
        depth = 1