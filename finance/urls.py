from django.urls import path

from finance.views import ChargeWalletView, VerifyView, PaymentView, PaymentGatewayView, SamplePaymentGatewayView,PaymentSampleView

urlpatterns = [
    path('charge/',ChargeWalletView.as_view() , name='payment'),
    path('verify/',VerifyView.as_view() , name='verify'),
    path('pay/<str:invoice_number>/',PaymentView.as_view() , name='payment-link'),
    path('pay/sample/<str:invoice_number>/',PaymentSampleView.as_view() , name='payment-link-sample'),# To pass Payment Portal and see how it works
    path('pay/<str:invoice_number>/<str:gateway_code>/',PaymentGatewayView.as_view() , name='payment-gateway'),
    path('pay/sample/<str:invoice_number>/<str:gateway_code>/',SamplePaymentGatewayView.as_view() , name='payment-gateway-sample'),# To pass Payment Portal and see how it works
 ]