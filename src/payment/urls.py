from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt

app_name = 'payment'

urlpatterns = [
    path('process/', views.payment_process, name='process'),
    path('confirmed/', views.payment_confirmed, name='confirmed'),
    path('conceled/', views.payment_canceled, name='canceled'),
]
