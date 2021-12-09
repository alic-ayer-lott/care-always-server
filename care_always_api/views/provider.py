from django.core.exceptions import ValidationError
from django.views.generic.base import View
from rest_framework import status
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from care_always_api.models import Question, Provider
from django.contrib.auth.models import User
from rest_framework.decorators import action

class ProviderView(ViewSet):

    def list(self,request):
        current_user = request.auth.user

        providers = current_user.providers.all()

        serializer = ProviderSerializer(
            providers, many=True, context={'request': request})
        return Response(serializer.data)
    
    def retrieve(self, request, pk=None):
        try:
            provider = Provider.objects.get(pk=pk)
            serializer = ProviderSerializer(provider, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)
    
    def create(self, request):

        current_user = request.auth.user

        try:
            provider = Provider.objects.create(
                first_name=request.data["first_name"],
                last_name=request.data["last_name"],
                specialty=request.data["specialty"],
                practice=request.data["practice"],
                address=request.data["address"],
                phone=request.data["phone"]
            )
            provider.patients.add(current_user)
            serializer = ProviderSerializer(provider, context={'request': request})
            return Response(serializer.data)
        
        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)
    
    def update(self, request, pk=None):

        provider = Provider.objects.get(pk=pk)

        provider.first_name=request.data["first_name"]
        provider.last_name=request.data["last_name"]
        provider.specialty=request.data["specialty"]
        provider.practice=request.data["practice"]
        provider.address=request.data["address"]
        provider.phone=request.data["phone"]

        provider.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)
    
    def destroy(self, request, pk=None):

        try:
            provider = Provider.objects.get(pk=pk)
            provider.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)
        
        except Provider.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
        
        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# class ProviderUserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ('id')


class ProviderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Provider
        fields = ('id', 'first_name', 'last_name', 'specialty', 'practice', 'address', 'phone')
        depth = 1