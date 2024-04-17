from django.shortcuts import render, redirect
import requests
import os
import logging
from urllib.parse import urlencode
from dotenv import load_dotenv
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.conf import settings
import time
import json
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import PaymentNotification
from django.http import QueryDict
from orders.models import SimpleOrder
from django.db import transaction

# Load environment variables
load_dotenv()

# Initialize logging
payments_logger = logging.getLogger('payments')

# Environment variables
BOIPA_MERCHANT_ID = os.getenv('BOIPA_MERCHANT_ID')
BOIPA_PASSWORD = os.getenv('BOIPA_PASSWORD')
BOIPA_TOKEN_URL = os.getenv('BOIPA_TOKEN_URL')  # URL to obtain the session token
PAYMENT_FORM_URL = os.getenv('HPP_FORM')  # URL for the payment form
HPP_FORM = os.getenv('HPP_FORM')


def home(request):
    # Render the home page. Additional context can be passed if needed.
    return render(request, 'home.html')


def get_boipa_session_token():
    # Create an order
    order = SimpleOrder(
        customer_name='John Doe',
        paid=True,
        total_cost=99.99
    )
    order.save()
    order_id = order.id

    order_ref = f'simple_{order_id}'
    print(order_ref)
    timestamp = time.strftime("%Y%m%d%H%M%S")
    # order_id = f"{base_order_id}_{timestamp}"

    url = BOIPA_TOKEN_URL  # UAT URL, change for production
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    payload = {
        "merchantId": settings.BOIPA_MERCHANT_ID,
        "password": settings.BOIPA_PASSWORD,
        "action": "AUTH",  # Based on the operation you're performing
        "timestamp": int(time.time() * 1000),  # Current time in milliseconds
        "allowOriginUrl": 'https://morganmck.eu.pythonanywhere.com/',  # Your ngrok URL for CORS
        "channel": "ECOM",
        "country": "IE",  # Example country code
        "currency": "EUR",  # Example currency
        "amount": "190.00",  # Example amount for AUTH or PURCHASE
        "merchantTxId": order_ref,  # Your internal order ID
        "merchantLandingPageUrl": "https://morganmck.eu.pythonanywhere.com//payment-response/",  # General callback URL for customer redirection
        "merchantNotificationUrl":"https://morganmck.eu.pythonanywhere.com//payment-notification/",  # Server-to-server notification URL(important
        # in case user makes a mess)
        "merchantLandingPageRedirectMethod": "GET",  # Ensure redirects use GET
    }

    response = requests.post(url, data=payload, headers=headers)
    if response.status_code == 200:
        return response.json().get('token')
    else:
        # Handle error
        print(f"Error obtaining session token: {response.text}")
        return None


def load_payment_form(request):
    token = get_boipa_session_token()
    if token is None:
        return render(request, 'error.html', {'error': 'Unable to obtain session token.'})

    # Construct the HPP URL with the obtained token and include integrationMode
    hpp_url = HPP_FORM + f"?token={token}&merchantId={settings.BOIPA_MERCHANT_ID}&integrationMode=Standalone"

    # Redirect user to the HPP URL
    return redirect(hpp_url)


def error_view(request):
    # Example error handling logic
    error_message = "An unexpected error has occurred."
    return render(request, 'error.html', {'error_message': error_message})


def payment_response(request):
    # Assuming 'result' is a parameter indicating the payment outcome
    payments_logger.debug(f"Received payment response: {request.GET.dict()}")
    result = request.GET.get('result')
    merchantTxId = request.GET.get('merchantTxId')
    if result == "success":
        # Message
        context = {
            'title': "Payment Success",
            'message': "Your payment has been successfully processed.",
            'order_ref': merchantTxId,
            'result': result,
        }
        return render(request, 'payment_success.html', context)

    elif result == "failure":
        # Logic for failed payment
        context = {
            'title': "Payment Failure",
            'message': f"Payment failed",
            'order_ref':merchantTxId,
            'result': result,
        }
        return render(request, 'payment_failure.html', context)

    else:
        # Handle unknown result
        return render(request, 'error.html', {'message': "Unknown payment response."})


@csrf_exempt  # Disable CSRF protection for this endpoint
def payment_notification(request):
    if request.method == 'POST':
        payments_logger.debug(f"Received payment notification: {request.POST.dict()}")
        # Parse the URL-encoded form data
        data = QueryDict(request.body)
        merchantTxId = data.get('merchantTxId')
        source_prefix, order_id_str = merchantTxId.split("_", 1)
        order_id = int(order_id_str)

    # Update Order
        with transaction.atomic():
            order = SimpleOrder.objects.get(id=order_id)
            order.paid = True
            order.save()
        # Store Notification Details
        with transaction.atomic():
            PaymentNotification.objects.create(
                order = order,
                txId=data.get('txId'),
                merchantTxId=data.get('merchantTxId'),
                country=data.get('country'),
                amount=data.get('amount'),
                currency=data.get('currency'),
                action=data.get('action'),
                # Assuming auth_code and other details are extracted correctly from paymentSolutionDetails or similar
                # auth_code=data.get('auth_code'),
                acquirer=data.get('acquirer'),
                acquirerAmount=data.get('acquirerAmount'),
                merchantId=data.get('merchantId'),
                brandId=data.get('brandId'),
                customerId=data.get('customerId'),
                acquirerCurrency=data.get('acquirerCurrency'),
                paymentSolutionId=data.get('paymentSolutionId'),
                status=data.get('status'),
            )
            payments_logger.info("Payment processed successfully.")
            # Return a successful HTTP response
            return HttpResponse('Payment processed successfully', status=200)

    # If not a POST request, or if other issues are encountered
    return HttpResponse('Invalid request', status=400)

