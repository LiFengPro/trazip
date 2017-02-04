from django.conf.urls import url

from frontier.views import home

urlpatterns = [
    url(r'^$', home.home, name='home'),
]