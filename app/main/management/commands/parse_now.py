import requests
from django.core.management.base import BaseCommand

from ... import models, check_offset_and_limit


class Command(BaseCommand):
    help = 'Run parsing data'

    def add_arguments(self, parser):
        parser.add_argument('-o', '--offset', default=0, type=int,
                            help='смещение по списку историй')
        parser.add_argument('-l', '--limit', default=30, type=int,
                            help='ограничение списка историй')

    def handle(self, offset: int, limit: int, *args, **options):
        """
        Парсинг новостей с сайта https://news.ycombinator.com/ с помощью предоставляемого API.

        :param offset: смещение по списку историй
        :param limit: ограничение списка историй
        :return: None
        """

        try:
            offset, limit = check_offset_and_limit(offset, limit)
        except TypeError as e:
            self.stdout.write(self.style.ERROR(e))

        top_stories = requests.get("https://hacker-news.firebaseio.com/v0/topstories.json").json()[offset:limit]

        def save_story(id: int, title: str, **kwargs):
            url = kwargs.get('url', f"https://news.ycombinator.com/item?id={id}")
            model = models.Posts(id=id, title=title, url=url)
            model.save()

            self.stdout.write(self.style.SUCCESS(f'Успешно сохранена история {model}'))

        for top_story in top_stories:
            response = requests.get(f"https://hacker-news.firebaseio.com/v0/item/{top_story}.json").json()
            save_story(**response)
