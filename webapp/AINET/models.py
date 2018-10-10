from django.db import models
from django.contrib.auth.models import User
import os

# Create your models here.

class Client(models.Model):
    name = models.CharField(max_length=30)
    website = models.URLField()
    email = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Site(models.Model):
    name = models.CharField(max_length=30)
    address = models.CharField(max_length=50)
    city = models.CharField(max_length=60)
    state_province = models.CharField(max_length=30)
    country = models.CharField(max_length=50)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Zone(models.Model):
    name = models.CharField(max_length=30)
    site = models.ForeignKey(Site, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.name

class Camera(models.Model):
    number = models.IntegerField()
    ref = models.IntegerField()
    maker = models.CharField(max_length=20)
    resolution = models.CharField(max_length=15)
    IP = models.URLField()
    port = models.IntegerField()
    zone = models.ForeignKey(Zone, on_delete=models.CASCADE)
    p1_x = models.IntegerField()
    p1_y = models.IntegerField()
    p2_x = models.IntegerField()
    p2_y = models.IntegerField()
    IOdirection = models.CharField(max_length=10)

    def __str__(self):
        return "Number : %i \n Maker : %s \n Resolution : %s \n Zone : %s" % (self.number, self.maker,
                                                                                 self.resolution, self.zone.__str__())


class Event(models.Model):
    SNAPSHOT_FOLDER = os.path.dirname(os.path.abspath(__file__))+'\db_images'
    type = models.CharField(max_length=100)
    time = models.DateTimeField()
    image = models.ImageField()
    camera = models.ForeignKey(Camera, on_delete=models.CASCADE)

    def __str__(self):
        return "%s at %s" % (self.type, str(self.time))   