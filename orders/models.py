from django.db import models

class SimpleOrder(models.Model):
    customer_name = models.CharField(max_length=100, verbose_name="Customer Name", default="Test")
    created = models.DateTimeField(auto_now_add=True, verbose_name="Created")
    updated = models.DateTimeField(auto_now=True, verbose_name="Updated")
    paid = models.BooleanField(default=False, verbose_name="Paid")
    total_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Total Price")

    class Meta:
        ordering = ('-created',)  # Orders records by creation time in descending order

    def __str__(self):
        return f'Order {self.id} - {self.customer_name}'

