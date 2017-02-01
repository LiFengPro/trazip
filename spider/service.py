import logging

from spider.ctrip import CtripHotels
from hotels.models import City, Hotel

class Service(object):

    def __init__(self):
        """Inits Service."""
        self.logger = logging.Logger('spider')


class CtripService(Service):
    """ All services supported scrapy from ctrip.com"""
    def update_cities(self):
        """Update all cities info in database."""
        cities = CtripHotels().get_cities()
        for city_data in cities:
            objs_in_db = City.objects.filter(ctrip_id=city_data['ctrip_id'])
            if objs_in_db:
                for obj in objs_in_db[1:]:
                    self.logger.critical('{} is duplicated and deleted'
                                         .format(obj))
                    obj.delete()
                if (objs_in_db[0].name != city_data['name'] or
                    objs_in_db[0].chinese_name != city_data['chinese_name']):
                    self.logger.critical('{} is changed to {}'.format(
                        objs_in_db[0], city_data))
                objs_in_db[0].name = city_data['name']
                objs_in_db[0].chinese_name = city_data['chinese_name']
                objs_in_db[0].save()
            else:
                city_obj = City(
                    name=city_data['name'],
                    ctrip_id=city_data['ctrip_id'],
                    chinese_name=city_data['chinese_name'])
                city_obj.save()

    def update_hotels(self):
        pass

    def update_rooms_and_prices(self):
        pass
