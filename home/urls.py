from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('load-payment-form/', views.load_payment_form, name='load_payment_form'),
    path('error/', views.error_view, name='error'),
    path('payment-success/', views.payment_success, name='payment-success'),
    path('payment-failure/', views.payment_failure, name='payment-failure'),
]
