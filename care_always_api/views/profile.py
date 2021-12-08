from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import serializers
from django.contrib.auth.models import User
from care_always_api.models import Appointment, Provider

@api_view(['GET'])
def user_profile(request):

    current_user = request.auth.user

    current_user = UserSerializer(
        current_user, context={'request': request}
    )

    #Construct JSON structure
    profile = {
        "current_user": current_user.data
    }

    return Response(profile)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email')