from xml.dom import ValidationErr
from django.contrib.auth.models import AbstractUser
from django.db import models

#from .validators import validate_file_extension

from accounts.managers import UserManager

GENDER_CHOICES = (
    ('male', 'Male'),
    ('female', 'Female'))

class User(AbstractUser):
    username = models.CharField(error_messages={'unique': 'A user with that username already exists.'}, max_length=150, unique=True, default = '')
    role = models.CharField(max_length=12, error_messages={
        'required': "Role must be provided"
    })
    gender = models.CharField(max_length=10, blank=True, null=True, default="")
    email = models.EmailField(unique=True, blank=False,
                              error_messages={
                                  'unique': "A user with that email already exists.",
                              })
    image = models.ImageField(default='',upload_to='profile_images')
    resume = models.FileField(default='', upload_to="resumes")
    province = models.CharField(max_length=50, null=True, blank=True)
    skill = models.CharField(max_length=500, null=True, blank=True)
    experience = models.CharField(max_length=500, null=True, blank=True)
    qualification = models.CharField(max_length=500, null=True, blank=True)


    
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ['email']

    def __unicode__(self):
        return self.email

    objects = UserManager()

class ActivityLog(models.Model):
    datetime = models.DateTimeField(auto_now_add=True)
    type = models.CharField(max_length=50, null=True)
    location = models.CharField(max_length=50, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    message = models.CharField(max_length=255, null=True, blank=True)
    
    def __str__(self) -> str:
        return f'{self.type} {self.location}'
    
    class Meta:
        ordering = ('-datetime',)
