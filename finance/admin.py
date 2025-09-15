from django.contrib import admin

from finance.models import Payment, GateWay

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('user', 'invoice_number', 'amount', 'gateway', 'is_paid', 'get_purchase_package_title' )

    def get_purchase_package_title(self, obj):
        return obj.purchase.package.title if obj.purchase and obj.purchase.package else "-"
    get_purchase_package_title.short_description = "Package Title"

admin.site.register(GateWay)