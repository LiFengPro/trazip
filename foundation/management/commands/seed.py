from django.core.management.base import BaseCommand

from spider.service import Service, CtripService

class Command(BaseCommand):
    help = 'Retrieve data to init database.'

    def handle(self, *args, **options):
        ctrip_service = CtripService()
        if ctrip_service.check_database_is_clean():
            self.stdout.write(self.style.SUCCESS(
                'Database is clean, start to generate data.'))
            cities_cnt = ctrip_service.update_cities()
            self.stdout.write(self.style.SUCCESS(
                '{} cities were generated and saved.'.format(cities_cnt)
            ))

            self.stdout.write(self.style.SUCCESS(
                'Gathering hotels info from ctrip.com, it may take several '
                'minutes.'
            ))
            for city_id in [1, 3]:
                for star in range(1, 6):
                    cnt = ctrip_service.update_hotels(city_id, star, 100)
                    self.stdout.write(self.style.SUCCESS(
                        '{} hotels were generated and saved.'.format(cnt)
                    ))
            ctrip_service.update_faked_rooms_and_prices()
            self.stdout.write(self.style.SUCCESS(
                'all hotels have faked room and price.'
            ))
        else:
            self.stderr.write(self.style.WARNING(
                'Warning: Database is not clean. '
            ))