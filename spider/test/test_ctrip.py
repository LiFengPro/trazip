from spider.ctrip import CtripHotels

class TestCtrip(object):
    def test_get_hotel_list(self):
        hotels = CtripHotels().get_hotel_list(city_id=2, star=5, counts=25)
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