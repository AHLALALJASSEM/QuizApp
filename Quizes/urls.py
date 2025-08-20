
from django.urls import path,include


from .views import CreatQuiz,GetQuizes,GetDetailForQuiz,EditQuiz,DeleteQuiz,GetQuizes_S

urlpatterns = [

         path("CreatQuiz/",CreatQuiz,name="CreatQuiz"),
         path("GetQuizes/<int:id>/",GetQuizes,name="GetQuizes"),
         path("GetQuizes_for_Student/<int:id>/",GetQuizes_S,name="GetQuizes_S"),
         path("GetDetailForQuiz/<int:id>/",GetDetailForQuiz,name="GetDetailForQuiz"),
         path("EditQuiz/<int:id>/",EditQuiz,name="EditQuiz"),
         path("DeleteQuiz/<int:id>/",DeleteQuiz,name="DeleteQuiz"),
         
]
