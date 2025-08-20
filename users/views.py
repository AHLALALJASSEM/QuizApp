from django.shortcuts import render
from rest_framework.decorators import api_view,permission_classes
from rest_framework.response import Response
from .serializers import UsersSerializer
from rest_framework.permissions import AllowAny
from .models import User
from djoser import utils
from django.http import HttpResponse



# Create your views here.

# Get All Users
@api_view(['GET'])
def Get_All_Users(request):
    Users = User.objects.all()
    Count_Users = User.objects.count()
    serializer = UsersSerializer(Users,many=True).data
    return Response({'Count_Users':Count_Users,'Users':serializer})

# Get All Users Sorted
@api_view(['GET'])
def Get_All_Users_Sorted(request):
    Teachers = User.objects.filter(role='Teacher')
    Students = User.objects.filter(role='Student')
    Admins = User.objects.filter(role='Admin')
    Count_Users = User.objects.count()
    serializer_Teachers = UsersSerializer(Teachers,many=True).data
    serializer_Students = UsersSerializer(Students,many=True).data
    serializer_Admins = UsersSerializer(Admins,many=True).data
    return Response({'Count_Users':Count_Users,
                    'Admins':serializer_Admins,
                     'Teachers':serializer_Teachers,
                     'Students':serializer_Students
                   })
    
@api_view(['POST'])
@permission_classes([AllowAny])
def ActivateAccount(request, pk,token):
    try:
        user = User.objects.get(pk=utils.decode_uid(pk))
    except User.DoesNotExist:
        return Response("User Not Found !!")
    if user :
        user.is_active = True
        user.save()
        return HttpResponse("The Account {} Is Activated Succesfully ".format(user.email))
    
    

    


