from django.shortcuts import render, redirect
import requests
import os
import logging
from urllib.parse import urlencode
from dotenv import load_dotenv
from django.http import HttpResponseRedirect
from django.conf import settings
import time
# Load environment variables
load_dotenv()

# Initialize logging
logger = logging.getLogger(__name__)

# Environment variables
BOIPA_MERCHANT_ID = os.getenv('BOIPA_MERCHANT_ID')
BOIPA_PASSWORD = os.getenv('BOIPA_PASSWORD')
BOIPA_TOKEN_URL = os.getenv('BOIPA_TOKEN_URL')  # URL to obtain the session token
PAYMENT_FORM_URL = os.getenv('HPP_FORM')  # URL for the payment form

def home(request):
    # Render the home page. Additional context can be passed if needed.
    return render(request, 'home.html')





def get_boipa_session_token():
    url = "https://apiuat.test.boipapaymentgateway.com/token"  # UAT URL, change for production
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    payload = {
        "merchantId": settings.BOIPA_MERCHANT_ID,
        "password": settings.BOIPA_PASSWORD,
        "action": "AUTH",  # Change based on the operation
        "timestamp": int(time.time() * 1000),  # Current time in milliseconds
        "allowOriginUrl": "https://7aa3-178-16-206-155.ngrok-free.app",  # Your ngrok URL
        "channel": "ECOM",
        "country": "IE",  # Example country code
        "currency": "EUR",  # Example currency
        "amount": "100.00",  # Example amount for AUTH or PURCHASE
        "merchantLandingPageUrl": "https://7aa3-178-16-206-155.ngrok-free.app/payment_success/",  # Your success callback URL
        "merchantNotificationUrl": "https://7aa3-178-16-206-155.ngrok-free.app/payment_failure/"  # Your failure callback URL or notification URL
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
    hpp_url = f"https://cashierui-apiuat.test.boipapaymentgateway.com/?token={token}&merchantId={settings.BOIPA_MERCHANT_ID}&integrationMode=Standalone"

    # Redirect user to the HPP URL
    return redirect(hpp_url)

def error_view(request):
    # Example error handling logic
    error_message = "An unexpected error has occurred."
    return render(request, 'error.html', {'error_message': error_message})

# Callback URLs
from django.http import HttpResponse

def payment_success(request):
    # Handle payment success logic here
    return HttpResponse("Payment successful.")

def payment_failure(request):
    # Handle payment failure logic here
    return HttpResponse("Payment failed.")