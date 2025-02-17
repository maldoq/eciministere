# models.py
from django.contrib.auth.models import User
from django.db import models


class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=40,default='',null=False)
    message = models.TextField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)

    def __str__(self):
        return f"Notification for {self.user.email}: {self.message}"
