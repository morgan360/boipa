from django.contrib import admin
# from .models import PaymentNotification


# @admin.register(PaymentNotification)
# class PaymentNotificationAdmin(admin.ModelAdmin):
#     list_display = ('tx_id', 'merchant_tx_id', 'amount', 'currency', 'status', 'data')
#     search_fields = ('tx_id', 'merchant_tx_id', 'status')
#     readonly_fields = ('data',)
#
#     def has_add_permission(self, request):
#         return False  # To prevent manual entries since these should only come from notifications
#
#     def has_change_permission(self, request, obj=None):
#         return False  # Optional: to prevent editing of notifications
#
#     def has_delete_permission(self, request, obj=None):
#         return True  # Depending on whether you want to allow deletion
