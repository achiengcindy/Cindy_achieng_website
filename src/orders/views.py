from django.shortcuts import render , redirect
from django.contrib.auth.decorators import login_required

from .models import OrderItem
from .forms import checkoutForm
from cart.cart import Cart

from django.urls import reverse #payment


@login_required
def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = checkoutForm(request.POST)
        if form.is_valid():
            order = form.save()
            for item in cart:
                OrderItem.objects.create(order=order,product=item['product'],price=item['price'],quantity=item['quantity'])
                # clear the cart
            cart.clear()
            # launch asynchronous task
            #order_created.delay(order.id)

            # set the order in the session
            request.session['order_id'] = order.id
            # redirect for payment
            return redirect(reverse('payment:validation'))
    else:
        form = checkoutForm()
    return render(request,'orders/order/create.html',{'cart': cart, 'form': form})




