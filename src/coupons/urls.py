from django.urls import path

from . import views

app_name = 'coupons'

urlpatterns = [
path('coupon/', views.coupon_include, name='include'),
]