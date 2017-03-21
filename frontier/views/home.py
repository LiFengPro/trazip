import logging

from django.shortcuts import render
from django.http import HttpResponse
from django.http import Http404

from foundation.models.city import City
from hotel.models.hotel import Hotel
from hotel.models.quotedprice import QuotedPrice
from hotel.models.room import Room

logger_test = logging.getLogger("trazip.frontier.test")

def home(request):
    try:
        city_1 = City.objects.get(ctrip_id=1)
        print("cccccccccccccccccccc")
        logger_test.info('aaaaaaaaaaaaaaa')
        logger_test.error('bbbbbbbb')
        #import pdb; pdb.set_trace()
        #print("city name is {}, id is {}".format(city_1.name, city_1.id))
    except City.DoesNotExist:
        raise Http404("Cannot find city where pk=1.")
    context = {
        'city': city_1,
    }
    return render(request, 'home/home.html', context)