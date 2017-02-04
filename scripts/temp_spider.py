# from django.conf import settings
# from trazip import settings as myapp_defaults
import django

# settings.configure(default_settings=myapp_defaults, DEBUG=True)
django.setup()

from spider.service import CtripService
print('This scrip is used for production and testing.')
CtripService().update_cities()


