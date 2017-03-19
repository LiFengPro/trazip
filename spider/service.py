import logging

from spider.ctrip import CtripHotels
from foundation.models.city import City
from hotel.models.hotel import Hotel
from hotel.models.room import Room
from hotel.models.quotedprice import QuotedPrice


class Service(object):

    def __init__(self):
        """Inits Service."""
        self.logger = logging.Logger('spider')

    def check_database_is_clean(self):
        """ Returns true if the database if in a clean state. """
        if City.objects.count() > 0:
            return False
        else:
            return True

class CtripService(Service):
    """ All services supported scrapy from ctrip.com"""

    def __init__(self):
        super().__init__()
        self.ctrip_hotels_spider = CtripHotels()

    def _delete_duplicate_objs(self, objs):
        for obj in objs[1:]:
            self.logger.ctitical('{} is duplicated and deleted'.format(obj))
            obj.delete()

    def _update_objs(self, obj, new_data):

        for key, value in new_data.items():
            if getattr(obj, key) != value:
                self.logger.critical('obj {} attr {} is changing from {} to {}.'
                    .format(obj, key, getattr(obj, key), value))
                setattr(obj, key, value)
            obj.save()


    def update_cities(self):
        """Update all cities info in database."""
        cities = self.ctrip_hotels_spider.get_cities()
        for city_data in cities:
            objs_in_db = City.objects.filter(ctrip_id=city_data['ctrip_id'])
            if objs_in_db:
                self._delete_duplicate_objs(objs_in_db)
                self._update_objs(objs_in_db[0], city_data)
            else:
                city_obj = City(**city_data)
                city_obj.save()
        return City.objects.count()

    def update_hotels(self, city_id='', star=0, counts=0):
        """ Update hotels info based on data from hotels.ctrip.com.

        Args:
            city_id (int): city_id in ctrip.com.
            star (int): Star of hotels, from 0 to 5
            counts (int): Numbers of hotels to get.
        """
        city = City.objects.get(pk=city_id)
        hotels = self.ctrip_hotels_spider.get_hotels(city_id, star, counts)
        for hotel_raw_data in hotels:
            hotel_data = {
                'ctrip_id': int(hotel_raw_data['id']),
                'address': hotel_raw_data['address'],
                'name': hotel_raw_data['name'],
                'level': star,
                'city': city,
                'rate': float(hotel_raw_data['score']),
                'description': ''
            }

            objs_in_db = Hotel.objects.filter(ctrip_id=hotel_data['ctrip_id'])
            if objs_in_db:
                self._delete_duplicate_objs(objs_in_db)
                self._update_objs(objs_in_db[0], hotel_data)
            else:
                hotel_obj = Hotel(**hotel_data)
                hotel_obj.save()

        return len(hotels)

    def update_faked_rooms_and_prices(self):
        """ Update faked rooms and prices of hotel.

        For test purpose, this method will generate faked rooms and prices
        for all existing hotels since getting price from ctrip.com is super
        slow.
        """

        import random
        random.seed(1234)
        hotels = Hotel.objects.all()

        room_names = ["大床房", "双人房", "总统套间", "商务大床房", "单人房"]

        for hotel in hotels:
            for room_name in room_names[0:random.randint(2, 5)]:
                room_data = {
                    'hotel': hotel,
                    'name': room_name,
                    'description': "",
                    "ctrip_id": random.randrange(1000000)
                }
                room_obj = Room(**room_data)
                room_obj.save()
                price_obj = QuotedPrice(
                    room = room_obj,
                    link = 'http://ctrip.com/{hotel_id}/{room_id}/{rand}'
                        .format(
                            hotel_id = hotel.ctrip_id,
                            room_id = room_obj.ctrip_id,
                            rand = random.randrange(1000000)
                        ),
                    price = 100 + random.randrange(1000)
                )
                price_obj.save()

    def update_rooms_and_prices(self):
        pass
