from django.db import models
from users.models import User

# Create your models here.



class Category(models.Model):
    name = models.CharField(max_length=50,unique=True)
    description = models.TextField(max_length=1000)
    date_created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User,on_delete=models.SET_NULL,null=True,to_field='id')
    
    
    REQUIRED_FIELDS=['name','description']
    
    
    
    def __str__(self):
        return self.name
    
    
    
    
