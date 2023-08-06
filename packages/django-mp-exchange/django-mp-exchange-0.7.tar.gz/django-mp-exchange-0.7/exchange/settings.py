
class ExchangeSettings(object):

    PRICE_MODEL = 'exchange.models.MultiCurrencyPrice'

    @property
    def INSTALLED_APPS(self):
        return super().INSTALLED_APPS + ['exchange']

    @property
    def CONTEXT_PROCESSORS(self):
        return super().CONTEXT_PROCESSORS + [
            'exchange.context_processors.currencies'
        ]
