from djoser.serializers import UserCreateSerializer
from rest_framework import serializers
from .models import User

class UserCreateSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        model=User
        fields=('id', 'email', 'name', 'password','role')
        
        

class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['name','email','role','is_active']
