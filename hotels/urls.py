from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^(?P<city>[0-9a-z]+)/$', views.hotel_list, name='hotel_list'),
]