import json
import uuid

from django.conf import settings
from django.db import models, transaction
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

import package
from finance.utils.zarinpal import zpal_request_handler
from purchase.models import Purchase


class GateWay(models.Model):
    """
    Save Gateways name and credentials to the db and use them to handle payments.
    """

    FUNCTION_SAMAN = 'saman'
    FUNCTION_SHAPARAK = 'shaparak'
    FUNCTION_FINOTHECH = 'finothech'
    FUNCTION_ZARINPAL = 'zarinpal'
    FUNCTION_PARSIAN = 'parsian'

    GATEWAY_FUNCTIONS = (
        (FUNCTION_SAMAN, _('Saman')),
        (FUNCTION_SHAPARAK, _('Shaparak')),
        (FUNCTION_FINOTHECH, _('Finothech')),
        (FUNCTION_ZARINPAL, _('Zarinpal')),
        (FUNCTION_PARSIAN, _('Parsian')),
    )

    title = models.CharField(max_length=120, verbose_name=_('gateway title'))
    gateway_request_url = models.CharField(max_length=120, verbose_name=_('request URL'), blank=True, null=True)
    gateway_verify_url = models.CharField(max_length=120, verbose_name=_('verify URL'), blank=True, null=True)
    gateway_code = models.CharField(max_length=120, verbose_name=_('gateway code'), choices=GATEWAY_FUNCTIONS)
    is_enable = models.BooleanField(verbose_name=_('is enable'), default=True)
    auth_data = models.TextField(verbose_name=_('auth data'), blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('Gateway')
        verbose_name_plural = _('Gateways')

    def __str__(self):
        return self.title

    def get_request_handler(self):
        handlers = {
            self.FUNCTION_SAMAN: None,
            self.FUNCTION_SHAPARAK: None,
            self.FUNCTION_FINOTHECH: None,
            self.FUNCTION_ZARINPAL: zpal_request_handler,
            self.FUNCTION_PARSIAN: None,
        }
        return handlers[self.gateway_code]

    def get_verify_handler(self):
        handlers = {
            self.FUNCTION_SAMAN: None,
            self.FUNCTION_SHAPARAK: None,
            self.FUNCTION_FINOTHECH: None,
            self.FUNCTION_ZARINPAL: zpal_request_handler,
            self.FUNCTION_PARSIAN: None,
        }
        return handlers[self.gateway_code]

    @property
    def credentials(self):
        return json.loads(self.auth_data)



class Payment(models.Model):
    invoice_number = models.UUIDField(verbose_name=_('invoice number'), default=uuid.uuid4, unique=True)
    amount = models.PositiveBigIntegerField(verbose_name=_('amount'), editable=True)
    gateway = models.ForeignKey(GateWay, on_delete=models.SET_NULL, related_name='payments', null=True, blank=True,
                                verbose_name=_('gateway')
                                )
    is_paid = models.BooleanField(verbose_name=_('is paid'), default=False)
    payment_log = models.TextField(verbose_name=_('payment log'), blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, related_name='payments', null=True,
                             verbose_name=_('user'),
    )
    authority = models.CharField(verbose_name=_('authority'), max_length=64, blank=True)
    purchase = models.ForeignKey(Purchase, on_delete=models.PROTECT, related_name='payments')

    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('Payment')
        verbose_name_plural = _('Payments')

    def __str__(self):
        return self.invoice_number.hex

    @staticmethod
    def create_purchase(package, user):
        purchase = Purchase.create(user=user, package=package)
        return purchase

    @classmethod
    def create(cls, package,user):
        with transaction.atomic():
            purchase = cls.create_purchase(user=user, package=package)
            payment = cls.objects.create(
                user=user,
                amount=purchase.price,
                purchase=purchase,
            )
        return payment, purchase

    def get_handler_data(self):
        return dict(
            merchant_id = self.gateway.auth_data, amount = self.amount, detail='',
            user_email = self.user.email, user_phone_number = getattr(self.user, 'user_phone_number', None),
            callback= 'https://127.0.0.1:8010/finance/verify'
        )

    @property
    def bank_page(self):
        handler = self.gateway.get_request_handler()
        if handler is not None:
            data = self.get_handler_data()
            link, authority = handler(**data)
            if authority is not None:
                self.authority = authority
                self.save()
            return link
        return None

    @property
    def title(self):
        return _('Instant payment')

    def status_changed(self):
        return self.is_paid != self._b_is_paid


    def verify(self, data):
        handler = self.gateway.get_verify_handler()
        if not self.is_paid and handler is not None:
            handler(**data)
            self.is_paid, _ = handler(**data)
        return self.is_paid

    def get_gateway(self):
        gateway = GateWay.objects.filter(is_enable = True).first()
        return gateway.gateway_code

    def save_log(self, data, scope="Request handler", save=True):
        generated_log = "[{}][{}] {}\n".format(timezone.now(), scope, data)
        if self.payment_log != '':
            self.payment_log += generated_log
        else:
            self.payment_log = generated_log
        if save:
            self.save()

