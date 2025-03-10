from django.contrib.auth.models import User  # Import the User model
from django.db import models


# Create your models here.
class Service(models.Model):
    libelleService = models.CharField(max_length=50)

    def __str__(self):
        return self.libelleService  # Return a string representation of the Service

class Agent(models.Model):
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='agents')  # Add related_name
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='agents', default=None)  # Add on_delete and related_name

    def __str__(self):
        return f"{self.user.username} - {self.service.libelleService}"  # Return a string representation of the Agent
