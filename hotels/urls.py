from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^(?P<city_name>[0-9a-z]+)/$', views.index, name='index'),

]