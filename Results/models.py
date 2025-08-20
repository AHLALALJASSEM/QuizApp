from django.db import models
from users.models import User


from Quizes.models import Quizes
from Question.models import Question

class Results(models.Model):
    Result = models.FloatField()
    Quiz = models.ForeignKey(Quizes,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    correct_questions = models.ManyToManyField(Question,related_name='correct')
    worng_questions = models.ManyToManyField(Question,related_name='worng')
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    
    
