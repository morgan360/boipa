# Generated by Django 5.0.3 on 2024-04-02 15:27

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('home', '0002_delete_paymentnotification'),
    ]

    operations = [
        migrations.CreateModel(
            name='PaymentNotification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('country', models.CharField(max_length=2)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('acquirer_tx_id', models.CharField(max_length=50)),
                ('tx_id', models.CharField(max_length=50)),
                ('language', models.CharField(max_length=5)),
                ('auth_code', models.CharField(max_length=10)),
                ('acquirer', models.CharField(max_length=100)),
                ('acquirer_amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('myriad_flow_id', models.CharField(max_length=50)),
                ('merchant_id', models.CharField(max_length=50)),
                ('brand_id', models.CharField(max_length=50)),
                ('merchant_tx_id', models.CharField(max_length=50)),
                ('customer_id', models.CharField(max_length=50)),
                ('acquirer_currency', models.CharField(max_length=3)),
                ('action', models.CharField(max_length=10)),
                ('payment_solution_id', models.IntegerField()),
                ('currency', models.CharField(max_length=3)),
                ('pan', models.CharField(max_length=16)),
                ('status', models.CharField(max_length=50)),
                ('original_tx_id', models.CharField(blank=True, max_length=50, null=True)),
            ],
        ),
    ]