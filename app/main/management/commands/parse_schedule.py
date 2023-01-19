import datetime
import time

from django.core.management.base import BaseCommand
from . import parse_now


class Command(parse_now.Command, BaseCommand):
    help = 'Run and schedule parsing data'

    def add_arguments(self, parser):
        parser.add_argument('-d', '--days', default=0, type=int,
                            help='таймер (по дням)')
        parser.add_argument('-H', '--hours', default=12, type=int,
                            help='таймер (в часах)')
        parser.add_argument('-m', '--minutes', default=0, type=int,
                            help='таймер (в минутах)')
        parser.add_argument('-s', '--seconds', default=0, type=int,
                            help='таймер (в секундах)')

        super().add_arguments(parser)

    def handle(self, days: int, hours: int, minutes: int, seconds: int, *args, **options):
        """
        Парсинг новостей с сайта https://news.ycombinator.com/ с помощью предоставляемого API
        с созданием последующего таймера.

        :param days: таймер (в днях)
        :param hours: таймер (в часах)
        :param minutes: таймер (в минутах)
        :param seconds: таймер (в секундах)
        :return: None
        """

        time_now = datetime.datetime.now()
        time_delta = datetime.timedelta(days=days, hours=hours, minutes=minutes, seconds=seconds)

        while True:
            super().handle(*args, **options)

            time_next = time_now + time_delta - datetime.datetime.now()
            self.stdout.write(self.style.SUCCESS(f'\n\nСледующая итерация через: {time_next}'))

            time.sleep(time_next.total_seconds())
