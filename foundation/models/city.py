from django.db import models

class City(models.Model):
    name = models.CharField(max_length=20)
    ctrip_id = models.IntegerField()
    chinese_name = models.CharField(max_length=20)

    def __repr__(self):
        return '{}|{}|{}'.format(self.ctrip_id, self.name, self.chinese_name)