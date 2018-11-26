from django.shortcuts import render , redirect
from django.contrib.auth.decorators import login_required

from .models import OrderItem
from .models import Order
from .forms import checkoutForm

from cart.cart import Cart

from django.urls import reverse #payment


@login_required
def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = checkoutForm(request.POST)
        if form.is_valid():
            order = Order.objects.create()
            #order.owner_id =  
            order = form.save()
            for item in cart:
                OrderItem.objects.create(order=order,product=item['product'],price=item['price'],quantity=item['quantity'])
                # clear the cart
            cart.clear()
            return render(request,'orders/order/created.html',{'order': order})
            
    else:
        form = checkoutForm()
    return render(request,'orders/order/create.html',{'cart': cart, 'form': form})



