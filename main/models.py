from __future__ import unicode_literals
from django.db import models

# Create your models here.

class Main(models.Model):
    name = models.CharField(max_length=34)
    about = models.TextField(default='-')
    abouttxt = models.TextField(default='')
    fb = models.CharField(max_length=34)
    tw = models.CharField(max_length=34)
    yt = models.CharField(max_length=34)
    tell = models.CharField(max_length=34)
    link = models.CharField(max_length=34)

    set_name = models.CharField(max_length=34)

    picurl = models.TextField(default='-')
    picname = models.TextField(default='-')
    picurl2 = models.TextField(default="")
    picname2 = models.TextField(default="")

    
    def __str__(self):
        return self.set_name + " | " + str(self.pk)
    
  

