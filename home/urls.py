from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('load-payment-form/', views.load_payment_form, name='load_payment_form'),
    path('error/', views.error_view, name='error'),
    # path('payment/notification/', views.payment_notification, name='payment_notification'),
    path('payment-notification/', views.payment_notification, name='payment-notification'),
    path('payment-response/', views.payment_response, name='payment-response'),
]
