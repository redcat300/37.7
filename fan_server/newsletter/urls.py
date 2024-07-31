from django.urls import path
from .views import subscribe, send_newsletter, subscription_success

urlpatterns = [
    path('subscribe/', subscribe, name='subscribe'),
    path('send_newsletter/', send_newsletter, name='send_newsletter'),
    path('subscription_success/', subscription_success, name='subscription_success'),
]
