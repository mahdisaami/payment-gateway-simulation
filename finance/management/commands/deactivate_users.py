from django.contrib.auth.models import User
from django.core.management import BaseCommand, CommandError


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('username', nargs='+', type = str,)

    def handle(self, **kwargs):
        usernames = kwargs['username']
        users = User.objects.filter(username__in = usernames)
        if users.exists():
            users.update(is_active = True)
            print(', '.join(users.values_list('username', flat=True)))

