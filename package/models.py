from django.db import models
from django.utils.translation import gettext_lazy as _

class Package(models.Model):
    title = models.CharField(verbose_name=_('title') , max_length=100)
    price = models.BigIntegerField(verbose_name=_('price'))
    description = models.TextField(verbose_name=_('description'))
    days = models.PositiveIntegerField(verbose_name=_('days'))
    months = models.PositiveSmallIntegerField(verbose_name=_('months'))
    is_enabled = models.BooleanField(verbose_name=_('is_enabled') , default=True)

    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('created_at'))
    modified_at = models.DateTimeField(auto_now=True, verbose_name=_('modified_at'))


    class Meta:
        verbose_name = _('package')
        verbose_name_plural = _('packages')

    def __str__(self):
        return self.title



class PackageAttribute(models.Model):
    package = models.ForeignKey(Package, on_delete=models.CASCADE, related_name='attributes',verbose_name=_('package'))
    title = models.CharField(max_length=100, verbose_name=_('title'))

    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('created_at'))
    modified_at = models.DateTimeField(auto_now=True, verbose_name=_('modified_at'))

    class Meta:

        verbose_name = _('package attribute')
        verbose_name_plural = _('package attributes')


    def __str__(self):
        return self.title

