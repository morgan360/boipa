import requests
import time
from decimal import Decimal
from django.urls import reverse
from .models import SimpleOrder
from django.conf import settings
import logging

payments_logger = logging.getLogger('payments')

def get_boipa_session_token(order_id, total_price):
    try:
        order = SimpleOrder.objects.get(id=order_id)
        amount = Decimal(f"{total_price:.2f}")

        order_ref = f'simple_{order_id}'

        url = settings.BOIPA_TOKEN_URL
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        payload = {
            "merchantId": settings.BOIPA_MERCHANT_ID,
            "password": settings.BOIPA_PASSWORD,
            "action": "PURCHASE",
            "timestamp": int(time.time() * 1000),
            "allowOriginUrl": settings.NGROK,
            "channel": "ECOM",
            "country": "IE",
            "currency": "EUR",
            "amount": str(amount),
            "merchantTxId": order_ref,
            "merchantLandingPageUrl": settings.NGROK + reverse('home:payment-response'),
            "merchantNotificationUrl": settings.NGROK + reverse('home:payment-notification'),
            "merchantLandingPageRedirectMethod": "GET",
            "userDevice": "DESKTOP",
            "merchantChallengeInd": "01",
            "merchantDecReqInd": "N",
            "freeText": "Optional extra transaction info",
            # "brandId": None,  # Include this if differentiating between brands in the same merchant account
        }

        payments_logger.debug("Sending payload to API: %s", {k: v for k, v in payload.items() if k != 'password'})
        response = requests.post(url, data=payload, headers=headers)
        if response.status_code == 200:
            return response.json().get('token')
        else:
            payments_logger.error("Error obtaining session token: HTTP Status %s: %s", response.status_code, response.text)
            return None
    except requests.RequestException as e:
        payments_logger.error("Network-related error when obtaining session token: %s", str(e))
        return None
    except Exception as e:
        payments_logger.error("Unexpected error when obtaining session token: %s", str(e))
        return None
