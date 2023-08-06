
from django.urls import path

from exchange import views


app_name = 'exchange'


urlpatterns = [

    path('set-currency/', views.set_currency, name='set-currency')

]
