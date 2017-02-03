from django.shortcuts import render
from django.http import HttpResponse
from django.http import Http404

from foundation.models.city import City

def home(request):
    try:
        city_1 = City.objects.get(pk=1)
    except City.DoesNotExist:
        raise Http404("Cannot find city where pk=1.")
    context = {
        'city': city_1,
    }
    return render(request, 'home.html', context)