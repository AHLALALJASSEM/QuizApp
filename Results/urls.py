
from django.urls import path
from .views import AddResult,MyResult,ViewResult
urlpatterns = [

       path('AddResult/<int:id>/',AddResult,name='AddResult'),
       path('MyResult/',MyResult,name='MyResult'),
       path('ViewResult/<int:id>/',ViewResult,name='ViewResult'),
         
]