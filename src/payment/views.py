from django.views import View
import requests, json
from requests.auth import HTTPBasicAuth
#https://devforgalaxy.github.io/en/2017/10/23/django-handle-json-request-en.html 
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404
from decimal import Decimal
from django.conf import settings
from orders.models import Order

""" To intergrate Mpesa api
1. generate tokens
2. register confirmation+ validation urls
3. simulate transaction """

# generating acess tokens
def safaricom_access_token():
    try:
        consumer_key = settings.consumer_key
        consumer_secret = settings.consumer_secret
        api_URL = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"
        response = requests.get(api_URL, auth=HTTPBasicAuth(consumer_key, consumer_secret))
        return response.json()['access_token']
        """ tokens = response.json()['access_token']
        return tokens """
    except:
        return None

# payment validation     
def payment_validation(request):
    order_id = request.session.get('order_id')
    order = get_object_or_404(Order, id=order_id)
    return  HttpResponse('helo data')

def payment_confirmed(request):
    return HttpResponse('confirmed')

def payment_canceled(request):
    return HttpResponse('canceled')


