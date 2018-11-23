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

#send json data using python requests
# register confirmation and validation urls
def saf_registration(self):
    host_name = "https://45946c94.ngrok.io/"
    access_token = safaricom_access_token()
    api_url = "http://sandbox.safaricom.co.ke/mpesa/c2b/v1/registerurl"
    # no need to specify content-type if using json
    #headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    headers = {"Authorization": "Bearer %s" % access_token}
    request = {"ShortCode": "600504","ResponseType": "confirmed","ConfirmationURL": host_name + "/payment/confirmed", "ValidationURL": host_name + "/payment/validation"}
    response = requests.post(api_url, json=request, headers=headers)
    print(response)
    return response.json()


# payment validation     
def payment_validation(request):
    order_id = request.session.get('order_id')
    order = get_object_or_404(Order, id=order_id)
    return  HttpResponse('helo data')

def payment_confirmed(request):
    host_name = "%s"%str(request.get_host())
    #use jsonresponse
    return JsonResponse({"results": 0, "ResultDesc": "The service was accepted successfully","ThirdPartyTransID": host_name})
    #the object JsonResponse default Content-Type is set as application/json, and it will serialize your data and return to client.

def payment_canceled(request):
    return HttpResponse('canceled')

#simulating transaction
def saf_simulation():
	host_name = "https://6ec449ce.ngrok.io"
	access_token = safaricom_access_token()
	api_url = "https://sandbox.safaricom.co.ke/mpesa/c2b/v1/simulate"
	headers = {"Authorization": "Bearer %s" % access_token}
	request = { 
		"ShortCode":"600000",
  		"CommandID":"CustomerPayBillOnline",
  		"Amount":"5666",
  		"Msisdn":"254708374149",
  		"BillRefNumber":"666888" 
  		}
	response = requests.post(api_url, json = request, headers=headers)
	return response.json()
