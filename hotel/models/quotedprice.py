from django.db import models

from hotel.models.room import Room

class QuotedPrice(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    link = models.URLField(max_length=200)
    price = models.DecimalField(max_digits=8, decimal_places=2)

    def __repr__(self):
        return "Price: {}\nRoom: {}".format(self.price, repr(self.room))
