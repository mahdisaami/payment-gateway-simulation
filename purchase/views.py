from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404, HttpResponse
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.cache import cache_page

from finance.models import Payment
from package.models import Package
from purchase.models import Purchase


class PurchaseCreateView(LoginRequiredMixin, View):

    def get(self, request, package_id, *args, **kwargs):
        try:
            package = Package.objects.get(pk=package_id)
        except Package.DoesNotExist:
            raise Http404

        payment, purchase = Payment.create(package=package, user=request.user)
        print(payment)
        return render(request, 'purchase/create.html', context={'payment': payment, 'purchase': purchase})

@cache_page(300)
def purchase_list(request, username=None):
    purchases = Purchase.objects.all()
    if username is not None:
        purchases = purchases.filter(user__username=username)
        if not purchases.exists():
            return HttpResponse('Sorry Username doesn\'t exist')
    print('View touched!!!')

    return render(request, 'purchase/list.html', context={'purchases': purchases})

@method_decorator(cache_page(300), name='dispatch')
class PurchaseListView(View):
    pass