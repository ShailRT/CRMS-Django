from unittest.util import _MAX_LENGTH
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class ClientUser(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=12, null=True, blank=True)
    company = models.CharField(max_length=120, null=True, blank=True)
    email = models.CharField(max_length=120, null=True, blank=True)
    
    def __str__(self):
        return self.user.username


    
    
