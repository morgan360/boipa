from django.db import models

class PaymentNotification(models.Model):
    country = models.CharField(max_length=2)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    acquirer_tx_id = models.CharField(max_length=50)
    tx_id = models.CharField(max_length=50)
    language = models.CharField(max_length=5)
    auth_code = models.CharField(max_length=10)  # Extracted from paymentSolutionDetails
    acquirer = models.CharField(max_length=100)
    acquirer_amount = models.DecimalField(max_digits=10, decimal_places=2)
    myriad_flow_id = models.CharField(max_length=50)
    merchant_id = models.CharField(max_length=50)
    brand_id = models.CharField(max_length=50)
    merchant_tx_id = models.CharField(max_length=50)
    customer_id = models.CharField(max_length=50)
    acquirer_currency = models.CharField(max_length=3)
    action = models.CharField(max_length=10)
    payment_solution_id = models.IntegerField()
    currency = models.CharField(max_length=3)
    pan = models.CharField(max_length=16)
    status = models.CharField(max_length=50)
    original_tx_id = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return self.tx_id
