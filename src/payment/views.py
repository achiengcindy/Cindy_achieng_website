from django.shortcuts import render, get_object_or_404
from decimal import Decimal
from django.conf import settings
from orders.models import Order



def payment_process(request):
    order_id = request.session.get('order_id')
    order = get_object_or_404(Order, id=order_id)
    host = request.get_host()
    consumer_key = settings.consumer_key
    consumer_secret =settings.consumer_secret

    if request.method == 'POST':
        mpesa_dict = {
            #'CommandID':,
            # amount to be transacted
            'Amount':'{:.2f}'.format(order.get_total_cost()),
            # phone no sending the trans start with country code without the (+) sign
            #'MSISDN':,
            'item_name': 'Order {}'.format(order.id),
            # optional invoice no
            'BillRefNumber': str(order.id),
            #'ShortCode':
        }
        if mpesa_dict.is_success:
            # mark the order as paid
            order.paid = True
            # store the unique transaction id
            order.braintree_id = result.transaction.id
            order.save()
            return redirect('payment:confirmed')
        else:
            return redirect('payment:canceled')
    else:
        # generate token 
        #client_token = braintree.ClientToken.generate()
        return render(request,'payment/process.html',{'order': order})

def payment_confirmed(request):
    return render(request, 'payment/confirmed.html')

def payment_canceled(request):
    return render(request, 'payment/canceled.html')

