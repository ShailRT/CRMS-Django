from django.db import models
from django.contrib.auth import get_user_model
import uuid
from client.models import ClientUser

User = get_user_model()

class OpsUser(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # id_user = models.IntegerField()

    def __str__(self):
        return self.user.username
    
class Campaign(models.Model):
    user = models.ForeignKey(OpsUser, on_delete=models.CASCADE)
    client = models.ForeignKey(ClientUser, on_delete=models.CASCADE)
    camp_name = models.CharField(max_length=50)
    course = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    quantity = models.IntegerField()
    sent = models.IntegerField(default=0)
    # file = models.FileField(upload_to='leads/%Y/%m/%d')
    
    def __str__(self):
        return f"{self.user} - {self.course} - {self.city}"

class Heap(models.Model):
    lead_id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=10)
    city = models.CharField(max_length=100)
    course = models.CharField(max_length=100)
    users = models.ManyToManyField(ClientUser, related_name="users", null=True, blank=True)

    

    def __str__(self):
        return self.name

class LeadFile(models.Model):
    lead_id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE)
    leads = models.FileField()
    quantity = models.IntegerField()
    date_created = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-date_created']

    def __str__(self):
        return f"{self.campaign} - {self.date_created}"

class UploadFile(models.Model):
    upload_id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    upload = models.FileField(upload_to='upload/')
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.date_created}"


    