from django.shortcuts import render, redirect
from .models import Refund
from .forms import RefundForm
from django.contrib import messages

def process_refund(request):
    if request.method == 'POST':
        form = RefundForm(request.POST)
        if form.is_valid():
            # Process refund here (e.g., calling an external API)
            # And then create a Refund record
            Refund.objects.create(
                transaction_id=form.cleaned_data['transaction_id'],
                amount=form.cleaned_data['amount'],
                reason=form.cleaned_data['reason']
            )
            messages.success(request, 'Refund processed successfully.')
            return redirect('some-view-name')
    else:
        form = RefundForm()
    return render(request, 'refunds/refund_form.html', {'form': form})

