from django.urls import path
from . import views

app_name = 'orders'


urlpatterns = [
    path('created/', views.order_created, name='order_created'),
    #path('created/<int:order_id>/', views.order_created, name='order_create'),
    
]


