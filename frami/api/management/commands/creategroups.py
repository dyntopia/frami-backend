from django.core.management.base import BaseCommand, CommandError

from ...groups import GroupError, create_groups


class Command(BaseCommand):
    def handle(self, *_args, **_options):
        try:
            create_groups()
        except GroupError as e:
            raise CommandError(e)
