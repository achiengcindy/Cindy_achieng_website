from django.shortcuts import render , redirect
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.urls import reverse #payment
import weasyprint
from django.conf import settings
from django.contrib.auth import get_user_model

from .models import OrderItem
from .models import Order
from .forms import BillingEditForm
#from cart.forms import CartAddProductForm

from cart.cart import Cart

User = get_user_model()

def order_create(request):
    return render(request,'orders/order/create.html',{})

@login_required
def order_created(request):
    cart = Cart(request)
    order= Order.objects.create()
    order.save()
    print(order)

    if cart.coupon:
        order.coupon = cart.coupon
        order.discount = cart.coupon.discount
    order.customer = request.user
    order.save()
    print(order)

    for item in cart:
        OrderItem.objects.create(order=order,product=item['product'],price=item['price'],quantity=item['quantity'])
    # clear the cart
    cart.clear()
    # set the order in the session
    #request.session['order_id'] = order.id
    return render(request,'orders/order/created.html',{'order': order, 'cart': cart})


""" @login_required
def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = checkoutForm(request.POST)
        if form.is_valid():
            order = Order.objects.create() 
            order = form.save(commit=False)
            if cart.coupon:
                order.coupon = cart.coupon
                order.discount = cart.coupon.discount
            order.customer = request.user
            order.save() 
            for item in cart:
                OrderItem.objects.create(order=order,product=item['product'],price=item['price'],quantity=item['quantity'])
            # clear the cart
            cart.clear()
            # set the order in the session
            request.session['order_id'] = order.id
            return render(request,'orders/order/created.html',{'order': order})
            
    else:
        form = checkoutForm()
    return render(request,'orders/order/create.html',{'cart': cart, 'form': form}) """




""" @staff_member_required
def admin_order_pdf(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    html = render_to_string('orders/order/pdf.html',{'order': order})

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="order_{}.pdf"'.format(order.id)
    weasyprint.HTML(string=html).write_pdf(response,stylesheets=[weasyprint.CSS(settings.STATIC_ROOT + 'css/pdf.css')])
    return response
 """





