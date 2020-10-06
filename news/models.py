from __future__ import unicode_literals
from django.db import models

# Create your models here.

class News(models.Model):
    name = models.CharField(max_length=34)
    short_txt = models.TextField(default='-')
    body_txt = models.TextField(default='-')
    date = models.CharField(max_length=34)
    time = models.CharField(max_length=34,default='00:00')
    picname = models.TextField(default='-')
    picurl = models.TextField(default='-')
    writer = models.CharField(max_length=34)
    catname = models.CharField(max_length=34,default='-')
    catid = models.IntegerField(default=0)
    ocatid = models.IntegerField(default=0)
    show = models.IntegerField(default=0)
    tag = models.TextField(default='')
    act = models.IntegerField(default=0)
    rand = models.IntegerField(default=0)
    
    def __str__(self):
         return self.name + " ||| " + str(self.pk)
    
  

