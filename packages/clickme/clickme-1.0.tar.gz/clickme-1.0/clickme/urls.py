from django.urls import path
from clickme.views import *

urlpatterns = [
    path('card/create/', CardCreateApiView.as_view(), name='card_create'),
    path('card/verify/', CardVerifyApiView.as_view(), name='card_verify'),
    path('payment/', PaymentApiView.as_view(), name='payment'),
]