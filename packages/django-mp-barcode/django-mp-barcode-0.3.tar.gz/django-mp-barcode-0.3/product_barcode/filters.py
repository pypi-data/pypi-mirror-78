
from django.utils.translation import ugettext_lazy as _

from cap.filters import InputFilter


class BarCodeFilter(InputFilter):

    parameter_name = 'bar_code'
    title = _('Bar code')

    def queryset(self, request, queryset):

        if not self.value():
            return

        return queryset.filter(bar_code=self.value())
