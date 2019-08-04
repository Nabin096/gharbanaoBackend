from django.db import models
from designers.models import *

# Create your models here.
class Job(models.Model):
    roomtype = models.CharField(max_length=15)
    lifespan = models.CharField(max_length=20)
    execution = models.BooleanField(default=False)
    area = models.FloatField()
    estimatedbudget = models.IntegerField()
    requirements = models.TextField(max_length=200,blank=True,null=True)
    email=models.EmailField(max_length=100)
    designer=models.ForeignKey(Designers,on_delete=models.CASCADE)
    job_started=models.BooleanField(default=False)
    password=models.CharField(max_length=50)
    name=models.CharField(max_length=100,null=True)
    contact=models.CharField(max_length=14,null=True)
    date=models.DateTimeField(default=datetime.now())

    def __str__(self):
       return self.email



class Complains(models.Model):
    to=models.ForeignKey(Designers, on_delete=models.CASCADE,blank=True,null=True)
    by=models.ForeignKey(Job,on_delete=models.CASCADE)
    complain=models.CharField(max_length=2000)
    date=models.DateField(default=datetime.now())


class Updates(models.Model):
    job=models.ForeignKey(Job,on_delete=models.CASCADE)
    author=models.CharField(max_length=100)
    date = models.DateTimeField(default=datetime.now())
    image=models.ImageField(null=True,blank=True)
    article=models.TextField(max_length=500)
    designer=models.BooleanField(default=False)

    def __str__(self):
       return self.article



