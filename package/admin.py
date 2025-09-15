
from django.contrib import admin

from package.models import Package, PackageAttribute

class PackageAttributeInline(admin.TabularInline):
    model = PackageAttribute
    list_display = ('title', 'value')
    search_fields = ('name',)


@admin.register(Package)
class PackageAdmin(admin.ModelAdmin):
    inlines = (PackageAttributeInline,)
    list_display = ('title', 'price', 'days')
    search_fields = ('title',)


