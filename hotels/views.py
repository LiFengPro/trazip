from django.shortcuts import render
from django.http import HttpResponse

from .models import Hotel

# Create your views here.

def hotel_list(request, city):

    hotels = Hotel.objects.filter(city=city)
    context = {
        'hotels': hotels,
    }
    return render(request, 'hotels/hotel_list.html', context)