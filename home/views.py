from django.shortcuts import render, redirect
import requests
import os
import logging
from urllib.parse import urlencode
from dotenv import load_dotenv
from django.http import HttpResponseRedirect
from django.conf import settings
import time
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET

# Load environment variables
load_dotenv()

# Initialize logging
logger = logging.getLogger(__name__)

# Environment variables
BOIPA_MERCHANT_ID = os.getenv('BOIPA_MERCHANT_ID')
BOIPA_PASSWORD = os.getenv('BOIPA_PASSWORD')
BOIPA_TOKEN_URL = os.getenv('BOIPA_TOKEN_URL')  # URL to obtain the session token
PAYMENT_FORM_URL = os.getenv('HPP_FORM')  # URL for the payment form
NGROK = os.getenv('NGROK')  # For ip tunnel from BOIPA
HPP_FORM = os.getenv('HPP_FORM')
base_order_id = "TCSP003"
timestamp = time.strftime("%Y%m%d%H%M%S")
order_id = f"{base_order_id}_{timestamp}"


def home(request):
    # Render the home page. Additional context can be passed if needed.
    return render(request, 'home.html')


def get_boipa_session_token():
    url = BOIPA_TOKEN_URL  # UAT URL, change for production
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    payload = {
        "merchantId": settings.BOIPA_MERCHANT_ID,
        "password": settings.BOIPA_PASSWORD,
        "action": "AUTH",  # Based on the operation you're performing
        "timestamp": int(time.time() * 1000),  # Current time in milliseconds
        "allowOriginUrl": NGROK,  # Your ngrok URL for CORS
        "channel": "ECOM",
        "country": "IE",  # Example country code
        "currency": "EUR",  # Example currency
        "amount": "100.00",  # Example amount for AUTH or PURCHASE
        "merchantTxId": order_id,  # Your internal order ID
        "merchantLandingPageUrl": NGROK + "/payment-response/",  # General callback URL for customer redirection
        "merchantNotificationUrl": NGROK + "/payment/notification/",  # Server-to-server notification URL(important
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


# @require_GET
# def payment_success(request):
#     # Extract parameters from the GET request, if needed for display or logging
#     order_id = request.GET.get('order_id')
#     status = request.GET.get('status')
#
#     # You might want to update the order status in your database here
#
#     # Render a success template, potentially passing order details
#     context = {'order_id': order_id, 'status': status}
#     return render(request, 'payment_success.html', context)
#
#
# @require_GET
# def payment_failure(request):
#     # Similarly, handle failure and extract any necessary information
#     order_id = request.GET.get('order_id')
#     message = request.GET.get('message')  # Assuming you expect a failure reason
#
#     # You might want to log this failure or notify someone
#
#     # Render a failure template, potentially passing failure details
#     context = {'order_id': order_id, 'message': message}
#     return render(request, 'payment_failure.html', context)


def payment_response(request):
    # Assuming 'result' is a parameter indicating the payment outcome
    result = request.GET.get('result')
    order_id = request.GET.get('merchantTxId')

    if result == "success":
        # Logic for successful payment
        context = {
            'title': "Payment Success",
            'message': "Your payment has been successfully processed.",
            'order_id': order_id,
            'result': result,
        }
        return render(request, 'payment_success.html', context)

    elif result == "failure":
        # Logic for failed payment
        message = request.GET.get('message')  # Assuming a failure message is passed
        context = {
            'title': "Payment Failure",
            'message': f"Payment failed. Reason: {message}",
            'order_id': order_id,
            'result': result,
        }
        return render(request, 'payment_failure.html', context)

    else:
        # Handle unknown result
        return render(request, 'error.html', {'message': "Unknown payment response."})
