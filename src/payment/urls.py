from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt

app_name = 'payment'

urlpatterns = [
    path('validation/', views.payment_validation, name='validation'),
    path('confirmed/', views.payment_confirmed, name='confirmed'),
    path('conceled/', views.payment_canceled, name='canceled'),
    path('registration/', views.saf_registration, name='registration'),
]
