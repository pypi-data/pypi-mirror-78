
from django.utils.translation import ugettext_lazy as _

from cap.decorators import short_description
from exchange.models import ExchangeRates


@short_description(_('Recalculate prices'))
def recalculate_prices(modeladmin, request, queryset):
    ExchangeRates.update_prices(queryset)
