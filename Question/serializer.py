from rest_framework import serializers
from .models import Question
from .models import Choices
from itertools import zip_longest



class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model=Question
        fields =['id','question_text','category','created_at','mark']
        
        
        

class ChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model=Choices
        fields=['id','choice_text','question','is_correct']
        
        
    def edit_choices(question, choices_new):
        choice_objs=Choices.objects.filter(question=question )
        if len(choice_objs)==len(choices_new):
         for choice_obj,choice_new in zip(choice_objs,choices_new):
              choice_new['question']=question.id
              new_choice = ChoiceSerializer(choice_obj,data=choice_new)
              if new_choice.is_valid():
                new_choice.save()
        else:
            ChoiceSerializer.delete_choices(question)
            for new_choice in choices_new:
                is_correct=False
                if new_choice['is_correct']=='true':
                  is_correct=True
                choice_new = Choices.objects.create(
                     choice_text=new_choice['choice_text'],
                     is_correct=is_correct,
                     question=question
                )
    def delete_choices(question):
        choices_dl =Choices.objects.filter(question=question)
        for choice_dl in choices_dl:
            choice_dl.delete()
        
        
            
    