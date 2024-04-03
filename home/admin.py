from django.contrib import admin
from .models import PaymentNotification


class PaymentNotificationAdmin(admin.ModelAdmin):
    list_display = (
        'tx_id', 'amount', 'acquirer_tx_id', 'auth_code', 'merchant_id', 'brand_id', 'merchant_tx_id', 'action',
        'payment_solution_id', 'status', 'original_tx_id')
    search_fields = ('tx_id', 'merchant_tx_id', 'customer_id', 'pan', 'status')


admin.site.register(PaymentNotification, PaymentNotificationAdmin)
