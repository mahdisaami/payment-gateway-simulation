from django.core.management import BaseCommand
from django.db.models import Sum, Count

from finance.models import Payment


class Command(BaseCommand):
    help = 'Get reports from finance'

    def handle(self, **kwargs):
        payments = Payment.objects.values('user').annotate(total=Sum('amount'))

        print(payments)