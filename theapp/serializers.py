from django.contrib.auth.models import Group, User
from rest_framework import serializers
from .models import AccessToken, RefreshToken, CustomUser


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'groups']


class CustomUserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username', 'email']
        
        
class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']
 

class TokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = RefreshToken
        fields = ['user', 'token', 'expired']