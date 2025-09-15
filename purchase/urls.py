from django.urls import path

from purchase.views import PurchaseCreateView, purchase_list

urlpatterns = [
    path('create/<int:package_id>/', PurchaseCreateView.as_view(), name='purchase-create'),
    path('list/<str:username>/', purchase_list, name='purchase-list'),
]