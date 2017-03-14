from django.db import models

from foundation.models.city import City

class Hotel(models.Model):
    name = models.CharField(max_length=100)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    description = models.CharField(max_length=200)
    level = models.IntegerField()
    ctrip_id = models.IntegerField()
    address = models.CharField(max_length=200)
    rate = models.FloatField()

    def __repr__(self):
        return ("ctrip_id: {ctrip_id}\nname: {name}\nlevel: "
                "{level}\naddress: {address}\n"
                .format(ctrip_id=self.ctrip_id, name=self.name,
                        level=self.level, address=self.address))
