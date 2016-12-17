import datetime

from spider.ctrip import CtripHotels

class TestCtrip(object):
    def test_get_hotels(self):
        hotels = CtripHotels().get_hotels(city_id=2, star=5, counts=25)
        for hotel in hotels:
            assert len(hotels) == 25

    def test_get_cities(self):
        cities = CtripHotels().get_cities()
        for city in cities:
            if city['ctrip_id'] == 1:
                city['name'] == 'Beijing'
                city['chinese_name'] == '北京'
                break
        else:
            assert False, 'Beijing is missing.'

    def test_get_rooms_and_prices(self):
        """ Verifies function get_rooms_and_prices is able to get room info
        and price info for specific hotel.
        """
        today = datetime.date.today()
        tomorrow = today + datetime.timedelta(days=1)
        checkin = today.isoformat()
        checkout = tomorrow.isoformat()
        rooms, quoted_prices = CtripHotels().get_rooms_and_prices(
            city_id=1, hotel_id=436187, checkin=today, checkout=checkout)
        assert 'RoomID' in rooms[0]
        assert rooms, 'Fail to find any room info'
        for room in rooms:
            assert room['RoomID'], 'Fail to find room id in {}'.format(room)

        assert quoted_prices, 'Fail to find quoted prices info'
        for price in quoted_prices:
            assert price['price'], 'Fail to find price in {}'.format(price)
