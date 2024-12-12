from django.db import models
from django.contrib.auth.models import User 

class Habit(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    body = models.TextField()
    days = models.JSONField(default=list)
    duration = models.PositiveIntegerField(default=1)
    streak = models.PositiveIntegerField(default=0)
    last_checked = models.DateTimeField(null=True, blank=True)
    checked = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title