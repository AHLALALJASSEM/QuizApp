


from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.apps import apps

@receiver(post_migrate)
def create_groups_and_permissions(sender, **kwargs):
  
    teachers_group, _ = Group.objects.get_or_create(name='Teachers')
    students_group, _ = Group.objects.get_or_create(name='Students')

    
    models_info = [
        ('Category', 'category'),
        ('Question', 'Question'),
        ('Choices', 'Question'),
        ('Quizes', 'Quizes'),
        ('Results', 'Results'),
    ]

    
    teacher_actions = ['add', 'change', 'delete', 'view']
    student_actions = ['view']
    teacher_permissions = []
    student_permissions = []

    
    def get_permissions(actions, model_name, app_label):
        model = apps.get_model(app_label, model_name)
        content_type = ContentType.objects.get_for_model(model)
        return [
            Permission.objects.get(content_type=content_type, codename=f'{action}_{model_name.lower()}')
            for action in actions
            if Permission.objects.filter(content_type=content_type, codename=f'{action}_{model_name.lower()}').exists()
        ]

    
  

    for model_name, app_label in models_info:
        teacher_permissions += get_permissions(teacher_actions, model_name, app_label)
        student_permissions += get_permissions(student_actions, model_name, app_label)

     
    teachers_group.permissions.set(teacher_permissions)
    students_group.permissions.set(student_permissions)

