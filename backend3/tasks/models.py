from django.db import models

# Create your models here.
class Task(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    effort_to_complete = models.IntegerField()
    due_date = models.DateField()
    user_id = models.IntegerField()
