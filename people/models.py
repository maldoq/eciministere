from django.contrib.auth.models import User  # Import the User model
from django.db import models

# Create your models here.
class People(models.Model):
    addressPeople = models.CharField(max_length=200)
    birthdayPeople = models.DateField(default=None)
    numberPeople = models.CharField(max_length=10)  # Keep as CharField if it includes non-numeric characters
    indicatorPeople = models.CharField(max_length=5,default='+225')
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='people', default=None)

    def __str__(self):
        return f"{self.user.username} - {self.numberPeople}"  # Return a string representation of the People instance