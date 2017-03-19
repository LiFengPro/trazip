import logging

from django.shortcuts import render
from django.http import HttpResponse
from django.http import Http404

from foundation.models.city import City
from hotel.models.hotel import Hotel
from hotel.models.quotedprice import QuotedPrice
from hotel.models.room import Room

logger = logging.getLogger('trazip')

def home(request):
    try:
        city_1 = City.objects.get(pk=1)
        logger.debug('Getting city object {}'.format(repr(city_1)))
    except City.DoesNotExist:
        raise Http404("Cannot find city where pk=1.")
    context = {
        'city': city_1,
    }
    return render(request, 'home/home.html', context)