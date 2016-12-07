from django.conf import settings
from oneclicktravel import settings as myapp_defaults
import django

settings.configure(default_settings=myapp_defaults, DEBUG=True)
django.setup()

from spider.service import Service
print('This scrip is used for production and testing.')
Service().update_cities_info_from_ctrip()


