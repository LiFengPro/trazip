""" This file is used to launch spider server.

For now we support 2 modes:
1. debug mode, which will run all services immediatelly in debug mode.
2. production mode, which will update the data accourding to schedule.

Usage can be found by executing:
python spider/server.py -h
"""

import time
import sys
import os
import json
import argparse

import django
import schedule

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

parser = argparse.ArgumentParser(description='Run spider server.')
parser.add_argument('--debug', action='store_true', help='Run on debug mode')

def setup_django():
    """ Setup environment to run django standalone. """
    sys.path.append(base_dir)
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'oneclicktravel.settings')
    django.setup()


def schedule_job():
    """ Schedule job according to schedule.json. """

    from spider.service import CtripService

    with open(os.path.join(base_dir, 'spider', 'schedule.json'), 'r') as f:
        schedules = json.loads(f.read())

    services = {
        'CtripService': CtripService,
    }

    for service_name, tasks in schedules.items():
        if service_name in services:
            service = services[service_name]()
            for task, plan in tasks.items():
                if plan[0] == 'day':
                    if plan[1]:
                        schedule.every().day.at(plan[1]).do(
                            getattr(service, task))
                    else:
                        schedule.every().day.do(getattr(service, task))
                else:
                    raise Exception("Fail to recognize schedule plan {}".format(plan))
        else:
            raise KeyError("Service {} is not defined".format(service_name))

def main(args):
    setup_django()
    schedule_job()

    if args.debug:
        schedule.run_all()
    else:
        while True:
            schedule.run_pending()
            time.sleep(1)

if __name__ == '__main__':
    args = parser.parse_args()
    main(args)



