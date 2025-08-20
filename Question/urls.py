
from django.urls import path
from .views import AddQuestion,GetQuestion_by_Category,EditQuestion,delete_question

urlpatterns = [
    path('AddQuestion/',AddQuestion,name='AddQuestion'),
    path('GetAllQuestin/<int:pk>/',GetQuestion_by_Category,name='GetQuestion'),
    path('EditQuestion/<int:pk>/',EditQuestion,name='EditQuestion'),
    path('DeleteQuestion/<int:pk>/',delete_question,name='DeleteQuestion')
]