
from django.urls import path,include
from .views import AddCategory,GetCategory,ModifyCategory,DeleteCategory,GetCategory_S


urlpatterns = [
     path('AddCategory/',AddCategory,name='AddCategory'),
     path('GetAllCategory/',GetCategory,name='GetCategory'),
     path('GetAllCategory_for_student/',GetCategory_S,name='GetCategory_S'),
     path('ModifyCategory/<int:pk>/',ModifyCategory,name='ModifyCategory'),
     path('DeleteCategory/<int:pk>/',DeleteCategory,name='DeleteCategory'),
]