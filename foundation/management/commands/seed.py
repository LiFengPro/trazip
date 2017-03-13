from django.core.management.base import BaseCommand

from spider.service import Service, CtripService

class Command(BaseCommand):
    help = 'Retrieve data to init database.'

    def handle(self, *args, **options):
        ctrip_service = CtripService()
        if ctrip_service.check_database_is_clean():
            self.stdout.write(self.style.SUCCESS(
                'Database is clean, start to generate data.'))
            cities_cnt = CtripService().update_cities()
            self.stdout.write(self.style.SUCCESS(
                '{} cities were generated and saved.'.format(cities_cnt)
            ))
        else:
            self.stderr.write(self.style.WARNING(
                'Warning: Database is not clean. '
            ))