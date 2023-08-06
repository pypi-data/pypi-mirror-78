
from django.shortcuts import redirect
from django.views.decorators.http import require_POST
from django.http.response import JsonResponse

from exchange.constants import CURRENCY_SESSION_KEY
from exchange.forms import CurrencyForm


@require_POST
def set_currency(request):

    form = CurrencyForm(request.POST)

    if not form.is_valid():
        return JsonResponse(form.errors.as_json())

    currency = form.cleaned_data['currency']

    request.session[CURRENCY_SESSION_KEY] = currency

    return redirect(request.GET.get('next', 'home'))