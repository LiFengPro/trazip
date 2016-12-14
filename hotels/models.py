from django.db import models

class City(models.Model):
    name = models.CharField(max_length=20)
    ctrip_id = models.IntegerField()
    chinese_name = models.CharField(max_length=20)


class Hotel(models.Model):
    name = models.CharField(max_length=40)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    description = models.CharField(max_length=200)
    level = models.IntegerField()
    ctrip_id = models.IntegerField()


class Room(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    name = models.CharField(max_length=20)
    description = models.CharField(max_length=200)
    ctrip_id = models.IntegerField()


class QuotedPrice(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    link = models.URLField(max_length=200)
    price = models.DecimalField(max_digits=8, decimal_places=2)