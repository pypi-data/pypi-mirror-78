
from django.contrib import admin

from solo.admin import SingletonModelAdmin

from exchange.models import ExchangeRates


@admin.register(ExchangeRates)
class ExchangeRatesAdmin(SingletonModelAdmin):

    list_display = ['id', 'usd', 'eur']
    list_editable = ['usd', 'eur']
