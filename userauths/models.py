from django.db import models
from django.contrib.auth.models import AbstractUser



# Create your models here.
class User(AbstractUser):
    email = models.EmailField(unique=True, null=False, blank=False)
    username = models.CharField(max_length=100)
    bio = models.CharField(max_length=100, null=True, blank=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    
    def __call__(self):
        return self.username

