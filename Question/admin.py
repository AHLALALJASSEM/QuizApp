from django.contrib import admin
from .models import Question
from .models import Choices
   
class ChoiceInline(admin.StackedInline):
    model = Choices
    extra = 4
        
class QuestionAdmin(admin.ModelAdmin):
    inlines=[ChoiceInline]
    

admin.site.register(Question,QuestionAdmin)
admin.site.register(Choices)
