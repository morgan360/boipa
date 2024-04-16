from django.contrib import admin
from .models import SimpleOrder


class SimpleOrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer_name', 'paid', 'created', 'updated', 'total_cost']
    list_filter = ['paid', 'created', 'updated']
    search_fields = ['customer_name']


admin.site.register(SimpleOrder, SimpleOrderAdmin)
