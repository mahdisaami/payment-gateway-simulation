from django.shortcuts import render
from django.views import View

from package.models import Package


class PricingView(View):

    def get_context_data(self, **kwargs):
        packages = Package.objects.filter(is_enabled=True)
        return {'packages': packages}

    def get(self,request, *args, **kwargs):
        return render(request, 'package/pricing.html', context=self.get_context_data(**kwargs))