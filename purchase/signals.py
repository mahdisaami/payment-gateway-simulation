from django.db.models.signals import post_save, post_init
from django.dispatch import receiver

from finance.models import Payment


@receiver(post_save, sender=Payment)
def callback(sender, instance, created, **kwargs):
    if instance.is_paid and not instance._b_is_paid:
        print("Signal is called!!!!")
        if instance.purchase:
            purchase = instance.purchase
            purchase.status = purchase.PAID
            purchase.save()


@receiver(post_init, sender=Payment)
def store_is_paid_status(sender, instance, **kwargs):
    print("Store is_paid_status is called!!!!")
    instance._b_is_paid = instance.is_paid