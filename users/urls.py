
from django.urls import path,include
from .views import Get_All_Users,Get_All_Users_Sorted,ActivateAccount

urlpatterns = [
    path('',include('djoser.urls')),
    path('',include('djoser.urls.jwt')),
    # path('All_Users/',Get_All_Users,name='Get_All_Users'), 
    # path('All_Users_Sort/',Get_All_Users_Sorted,name='Get_All_Users_Sorted'),
    path('activate/<str:pk>/<str:token>/',ActivateAccount,name="ActivateAccount")   
]