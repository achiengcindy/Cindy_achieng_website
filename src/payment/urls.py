from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt

app_name = 'payment'

urlpatterns = [
    path('lipa/', views.payment_lipa, name='lipa'),
    path('validation/', views.payment_validation, name='validation'),
    path('confirmed/', views.payment_confirmed, name='confirmed'),
    path('simulate/', views.saf_simulation, name='simulate'),
    path('registration/', views.saf_registration, name='registration'),
]
