from django.db import models

from foundation.models.city import City

class Hotel(models.Model):
    name = models.CharField(max_length=40)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    description = models.CharField(max_length=200)
    level = models.IntegerField()
    ctrip_id = models.IntegerField()
    address = models.CharField(max_length=200)
    rate = models.FloatField()

    def __repr__(self):
        return ("ctrip_id: {ctrip_id}\nname: {name}\nlevel: {}\naddress: {}\n"
                .format(ctrip_id=ctrip_id, name=name, level=level,
                        address=address))