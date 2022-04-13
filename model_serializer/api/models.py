from django.db import models
import uuid

# Create your models here.
class Student(models.Model):
    id = models.BigAutoField
    name = models.CharField(max_length=50)
    roll = models.IntegerField(unique=True)
    city = models.CharField(max_length=50, null=True)
