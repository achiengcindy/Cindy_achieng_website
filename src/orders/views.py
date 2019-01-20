
from django.shortcuts import render , redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.urls import reverse #payment
#import weasyprint
from django.conf import settings
from django.contrib.auth import get_user_model

from .models import OrderItem
from .models import Order
from accounts.models import Profile
from .forms import checkoutForm
#from cart.forms import CartAddProductForm
from cart.cart import Cart

User = get_user_model()


def order_create(request):
    """ we will obtain the current cart from the session """
    cart = Cart(request)
    if request.method == 'POST':
        form = checkoutForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            if cart.coupon:
                order.coupon = cart.coupon
                order.discount = cart.coupon.discount
            if request.user.is_authenticated:
                order.owner = request.user
            order.status = Order.SUBMITTED
            order.save()
            for item in cart:
                OrderItem.objects.create(order=order,
                                         product=item['product'],
                                         price=item['price'],
                                         quantity=item['quantity'])
            # clear the cart
            cart.clear()
            # launch asynchronous task
            #order_created.delay(order.id)
            # set the order in the session
            # request.session['order_id'] = order.id
            # redirect to the payment
            return render(request, 'orders/order/created.html',{"order": order, 'cart': cart,})
            #return redirect(reverse('orders:order_created',kwargs={"order_id": order.id, 'cart': cart,}))
    else:
        if request.user.is_authenticated:
            profile = request.user.profile
            form = checkoutForm(instance=profile)
        else:
            form = checkoutForm()
    return render(request, 'orders/order/create.html', {'cart': cart,'form':form})

# @login_required
# def order_created(request,order_id):
#     order.id = request.session['order_id']
#     if order_id:
#         order = Order.objects.get(id=order_id)
        
#     # # set the order in the session
#     # request.session['order_id'] = order.id
#     # # redirect to the payment
#     return render(redirect,'orders/order/created.html')

@login_required
def order_created(request,order_id):
    order = get_object_or_404(Order, id=order_id)
    # set the order in the session
    request.session['order_id'] = order.id
    return render(request,'orders/order/created.html',{'order': order})
    # redirect to the payment
    #return redirect(reverse('payment:payment_lipa', kwargs={"order_id": order.pk}))















""" @staff_member_required
def admin_order_pdf(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    html = render_to_string('orders/order/pdf.html',{'order': order})

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="order_{}.pdf"'.format(order.id)
    weasyprint.HTML(string=html).write_pdf(response,stylesheets=[weasyprint.CSS(settings.STATIC_ROOT + 'css/pdf.css')])
    return response
 """










