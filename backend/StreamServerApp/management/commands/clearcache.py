from django.core.management.base import BaseCommand
from django.core.cache import cache
from StreamingServer.celery import celery_app


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        cache.clear()
        celery_app.control.purge()
        self.stdout.write('Cleared cache and purged celery\n')
        