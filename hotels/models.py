from django.db import models

# Create your models here.
class Hotel(models.Model):
    name = models.CharField(max_length=40)
    city = models.CharField(max_length=10)
    description = models.CharField(max_length=200)
    level = models.IntegerField()


class Room(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    name = models.CharField(max_length=20)
    description = models.CharField(max_length=200)


class QuotedPrice(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    link = models.URLField(max_length=200)
    price = models.DecimalField(max_digits=8, decimal_places=2)