from django.conf import settings
from django.http import Http404
from django.shortcuts import render, redirect
from django.views import View

from finance.forms import ChargeWalletForm
from finance.models import Payment, GateWay
from finance.utils.zarinpal import zpal_request_handler, zpal_payment_checker


class ChargeWalletView(View):
    template_name = 'finance/charge_wallet.html'
    form_class = ChargeWalletForm

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {'form': self.form_class})

    def post(self, request, *args, **kwargs):   # Here we should store data in DB like amount, authority etc.
        form = self.form_class(request.POST)

        if form.is_valid():
            payment_link, authority = zpal_request_handler(
                settings.ZARINPAL['merchant_id'], form.cleaned_data['amount'],
                'Wallet charge', 'mahdisaami7828@gmail.com', None,
                settings.ZARINPAL['gateway_callback_url']
            )
            if payment_link is not None:
                print(authority)
                print(payment_link)
                return redirect(payment_link)
        return render(request, self.template_name, {'form': form})



class VerifyView(View):
    template_name = 'finance/callback.html'

    def get(self, request, *args, **kwargs):    # Here we should get the amount from the DB.
        authority = request.GET.get('Authority')
        try:
            payment = Payment.objects.get(authority=authority)
        except Payment.DoesNotExist:
            raise Http404
        data = dict(merchant_id=payment.gateway.auth_data, amount=payment.amount,authority=payment.authority )
        payment.verify(data)
        return render(request, self.template_name, {'payment': payment})



class PaymentView(View):

    def get(self, request,invoice_number, *args, **kwargs):
        try:
            payment = Payment.objects.get(invoice_number=invoice_number)
        except Payment.DoesNotExist:
            raise Http404

        gateways = GateWay.objects.filter(is_enable = True)
        return render(request, 'finance/payment_detail.html', {'payment': payment, 'gateways': gateways})


# To pass Payment Portal and see how it works
class PaymentSampleView(View):

    def get(self, request,invoice_number, *args, **kwargs):
        try:
            payment = Payment.objects.get(invoice_number=invoice_number)
        except Payment.DoesNotExist:
            raise Http404

        gateways = GateWay.objects.filter(is_enable = True)
        return render(request, 'finance/payment_detail_sample.html', {'payment': payment, 'gateways': gateways})


class PaymentGatewayView(View):

    def get(self, request,invoice_number,gateway_code, *args, **kwargs):
        try:
            payment = Payment.objects.get(invoice_number=invoice_number)
        except Payment.DoesNotExist:
            raise Http404

        try:
            gateway = GateWay.objects.get(gateway_code = gateway_code)
        except GateWay.DoesNotExist:
            raise Http404



        payment.gateway = gateway
        payment.save()
        payment_link = payment.bank_page
        if payment_link is not None:
            return redirect(payment_link)
        gateways = GateWay.objects.filter(is_enable = True)
        return render(request, 'finance/payment_detail.html', {'payment': payment, 'gateways': gateways})


# To pass Payment Portal and see how it works
class SamplePaymentGatewayView(View):
    def get(self, request, invoice_number, gateway_code, *args, **kwargs):
        try:
            payment = Payment.objects.get(invoice_number=invoice_number)
        except Payment.DoesNotExist:
            raise Http404

        try:
            gateway = GateWay.objects.get(gateway_code=gateway_code)
        except GateWay.DoesNotExist:
            raise Http404

        payment.gateway = gateway
        payment.is_paid = True
        payment.save()
        payment_link = 'callback'
        if payment_link is not None:
            return render(request, 'finance/callback.html', {'payment': payment})
        gateways = GateWay.objects.filter(is_enable=True)
        return render(request, 'finance/payment_detail.html', {'payment': payment, 'gateways': gateways})