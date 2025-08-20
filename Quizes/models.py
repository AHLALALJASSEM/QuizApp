from django.db import models
from Question.models import Question
from category .models import Category



lv=(
    ('Simple','Simple'),
    ('Intermidate','Intermidate'),
    ('Advanced','Advanced')
)

class Quizes(models.Model):
    title=models.CharField(max_length=255)
    description=models.TextField(max_length=2000)
    lv=models.CharField(choices=lv,max_length=20)
    count_questions=models.IntegerField()
    mark_total=models.FloatField()
    duration_minutes= models.IntegerField()
    created_at=models.DateTimeField(auto_now_add=True)
    questions=models.ManyToManyField(Question)
    category=models.ForeignKey(Category,on_delete=models.CASCADE)
    
    
    REQUIRED_FIELDS =['title','description','duration_minutes','category']
    
    
    def __str__(self):
        return self.title
    

    
    

