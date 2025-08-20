from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser,Group



roles = [
    ('Teacher' , 'Teacher' ),
    ('Student' , 'Student' ),
]

# Custom User Manager
class UserManager(BaseUserManager):
    def create_user(self, email, name,role, is_active=False, is_admin=False, password=None):
        """
        Creates and saves a User with the given email, name and password.
        """
        if not email:
            raise ValueError('User must have an email address')
        user = self.model(
            email=self.normalize_email(email),
            name=name,
            is_admin=is_admin,
            is_active=is_active,
            role=role
        )
        user.set_password(password)
        user.save(using=self._db)
        group_students = Group.objects.get(name = 'Students')
        group_teachers = Group.objects.get(name = 'Teachers')
        if role == 'Teacher':
            user.groups.add(group_teachers)
        if role == 'Student':
            user.groups.add(group_students)    
        return user
    def create_superuser(self, email,role, name,is_admin=True, is_active=True, password=None):
        """
        Creates and saves a Superuser with the given email, name and password.
        """
        user = self.create_user(
            email=email,
            password=password,
            name=name,
            is_active=is_active,
            is_admin=is_admin,
            role=role
        )
        user.is_admin = True
        user.save(using=self._db)
        return user

# Custom User Model.
class User(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='Email',
        max_length=255,
        unique=True,
    )
    name = models.CharField(max_length=255)
    role = models.TextField(max_length=255,choices=roles)
    is_active=models.BooleanField(default=False)
    is_admin=models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    groups = models.ManyToManyField("auth.Group")

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS=['name','role']

    def __str__(self):
        return self.email

    def get_full_name(self):
        return self.name

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return self.is_admin

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin
    
    
    


