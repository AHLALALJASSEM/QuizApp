from django.db import models
from django.contrib import admin
from category.models import Category
from rest_framework.response import Response




class Question(models.Model):
    question_text=models.TextField(max_length=5000)
    category=models.ForeignKey(Category,on_delete=models.CASCADE,to_field='id')
    created_at=models.DateTimeField(auto_now_add=True)
    mark=models.FloatField(default=2.5)
    
    
    REQUIRED_FIELDS =['question_text','mark','category']
    
    
    def __str__(self):
        return self.question_text
    
    def create_choices(choices,question):
          for choice  in choices:
              is_correct=False
              if choice['is_correct']=='true':
                is_correct=True
              Choices.objects.create(
               choice_text=choice['choice_text'],
               is_correct=is_correct,
                question=question
        )
        
    
    def get_choices(self, id):
        choice_objs=Choices.objects.filter(question = id)
        data=[]
        for choice_obj in choice_objs:
          data.append(
          {
              "id":choice_obj.id,
              "Choice_Text":choice_obj.choice_text,
              
          }
                 )
    
        return data
    def get_correct_choice(id):
                choice_obj = Choices.objects.get(question = id , is_correct = True)
                id_correct = choice_obj.id
                return id_correct
                
  
        
        
        
        
           
class Choices(models.Model):
    choice_text=models.TextField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)
    question=models.ForeignKey(Question,on_delete=models.CASCADE,related_name='Answers')
    is_correct=models.BooleanField(default=False)
    
    
    REQUIRED_FILDES =['choice_text','question','is_correct']
    
    def __str__(self):
        return self.choice_text
    
    
    

    
    
    
    
    
    
   
    
    
    
    
