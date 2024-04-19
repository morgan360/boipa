from django.shortcuts import render, redirect
from django.conf import settings
from django.http import HttpResponse, QueryDict
from django.db import transaction
from django.views.decorators.csrf import csrf_exempt
import logging
from .models import PaymentNotification, SimpleOrder
from .payment_functions import get_boipa_session_token  # If external functions are used
from django.conf import settings

# Initialize logging
payments_logger = logging.getLogger('payments')


def home(request):
    # Render the home page. Additional context can be passed if needed.
    return render(request, 'home.html')


def load_payment_form(request):
    # Create an order
    order = SimpleOrder(
        customer_name='John Doe',
        paid=False,
        total_price=99.99
    )
    order.save()
    total_price = 199.00
    order_id = order.pk
    token = get_boipa_session_token(order_id, total_price)
    if token is None:
        return render(request, 'error.html', {'error': 'Unable to obtain session token.'})

    # Construct the HPP URL with the obtained token and include integrationMode
    hpp_url = settings.HPP_FORM + f"?token={token}&merchantId={settings.BOIPA_MERCHANT_ID}&integrationMode=Standalone"

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
        payments_logger.info(f"Payment for {merchantTxId} processed successfully.")
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
        payments_logger.warning(f"Payment for {merchantTxId} failed.")
        context = {
            'title': "Payment Failure",
            'message': f"Payment failed",
            'order_ref': merchantTxId,
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
                order=order,
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
