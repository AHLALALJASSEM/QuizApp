from rest_framework import permissions 
from .models import User
from django.contrib.auth.models import Group
   
   
class Is_Teacher(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name="Teachers").exists()
    
    
    
class Is_Student(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name="Students").exists()