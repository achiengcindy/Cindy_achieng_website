from django.db import models
from shop.models import Product
from django.conf import settings
from django.contrib.auth import get_user_model

from decimal import Decimal
from django.core.validators import MinValueValidator, MaxValueValidator
from coupons.models import Coupon

from django.urls import reverse

User = get_user_model()

class OrderDetails(models.Model):
	""" stores customer order information used with the last order placed; can be attached to the checkout order form
    as a convenience to registered customers who have placed an order in the past.
    """
	class Meta:
		abstract = True

	# contact info
	phone = models.CharField(max_length=20)
	#shipping information
	physical_address =  models.CharField(max_length=250)
	postal_code = models.CharField(max_length=20)
	city = models.CharField(max_length=100)
	Estate = models.CharField(max_length=100)



class Order(OrderDetails):
    # each individual status
    SUBMITTED = 1
    PROCESSED = 2
    SHIPPED = 3
    CANCELLED = 4
    # set of possible order statuses
    ORDER_STATUS = (
        (SUBMITTED,'Submitted'),
        (PROCESSED,'Processed'),
        (SHIPPED,'Shipped'),
        (CANCELLED,'Cancelled'),
        )
    # order info
    owner = models.ForeignKey(User,on_delete=models.CASCADE, null=True, blank=True, related_name='orders')
    status = models.IntegerField(choices=ORDER_STATUS, default=SUBMITTED)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    paid = models.BooleanField(default=False)
    Mpesa_transid = models.CharField(max_length = 150, blank= True)
    coupon = models.ForeignKey(Coupon,related_name='orders',null=True,blank=True,on_delete=models.SET_NULL)
    discount = models.IntegerField(default=0,validators=[MinValueValidator(0),MaxValueValidator(100)])


    class Meta:
        ordering = ('-created',)
        verbose_name = "order"
        verbose_name_plural = "orders"

    def __str__(self):
        return 'Order {}'.format(self.id)

    """ def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all()) """

    def get_total_cost(self):
        total_cost = sum(item.get_cost() for item in self.items.all())
        return total_cost - total_cost * (self.discount / Decimal('100'))

    def get_absolute_url(self):
        return reverse('orders:order_create',args=[self.id, self.slug])

 

class OrderItem(models.Model):
    order = models.ForeignKey(Order,related_name='items',on_delete=models.CASCADE)
    product = models.ForeignKey(Product,related_name='order_items',on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return '{}'.format(self.id)

    def get_cost(self):
        return self.price * self.quantity

 








