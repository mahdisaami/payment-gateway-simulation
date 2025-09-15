from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy as _

from package.models import Package


class Purchase(models.Model):
    PAID = 10
    NO_PAID = -10

    STATUS_CHOICES = (
        (PAID, _('Paid')),
        (NO_PAID, _('No Paid')),
    )

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name=_('user'))
    package = models.ForeignKey(Package, on_delete=models.SET_NULL, null=True, related_name='purchases', verbose_name=_('package'))
    price = models.PositiveBigIntegerField(verbose_name=_('price'))
    status = models.SmallIntegerField(choices=STATUS_CHOICES, default=NO_PAID, verbose_name=_('status'))

    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('created at'))
    modified_at = models.DateTimeField(auto_now=True,verbose_name=_('modified at'))

    class Meta:
        verbose_name = _('purchase')
        verbose_name_plural = _('purchases')

    def __str__(self):
        return f'{self.user.username} ==> {self.package}'



    @classmethod
    def create(cls, package, user):
        if package.is_enabled:
            return cls.objects.create(user=user, package=package, price=package.price)
        return None

