
from urllib.parse import urlencode

from django.urls import reverse_lazy
from django.contrib import admin
from django.contrib import messages
from django.shortcuts import render, redirect
from django.utils.translation import ugettext_lazy as _

from product_barcode.models import BarCode


@admin.register(BarCode)
class BarCodeAdmin(admin.ModelAdmin):

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


@admin.site.register_view(
    'barcode/generate/',
    _('Generate bar codes'),
    'generate-bar-codes')
def generate_codes(request):

    context = admin.site.each_context(request)

    if request.method == 'POST':
        try:
            count = int(request.POST['count'])
            codes = BarCode.get_solo().get_next_codes(count)
            url = reverse_lazy('barcode:print')
            url += '?' + urlencode({'codes': ','.join(map(str, codes))})
        except Exception:
            messages.error(request, _('Incorrect number'))
            url = request.path

        return redirect(url)

    return render(request, 'barcode/generate.html', context)
