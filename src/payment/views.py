from django.views import View
import requests, json
from requests.auth import HTTPBasicAuth
#https://devforgalaxy.github.io/en/2017/10/23/django-handle-json-request-en.html 
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404
from decimal import Decimal
from django.conf import settings
from orders.models import Order

from django.views.decorators.csrf import csrf_exempt


""" To intergrate Mpesa api
1. generate tokens
2. register confirmation+ validation urls
3. simulate transaction """

def payment_lipa(request):
    order = get_object_or_404(Order, id=order_id)

    if(order.paid == True):
        return HttpResponse( "The payment was accepted successfully")
    else:
        return HttpResponse('payment didnt go through')
        
    

   

# generating acess tokens
def safaricom_access_token():
    try:
        consumer_key = 'settings.consumer_key'
        consumer_secret = 'settings.consumer_secret'
        api_URL = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"
        response = requests.get(api_URL, auth=HTTPBasicAuth(consumer_key, consumer_secret))
        return response.json()['access_token']
    except:
        return None

#send json data using python requests
# register confirmation and validation urls
def saf_registration(request):
    host = request.get_host()
    access_token = safaricom_access_token()
    api_url = "https://sandbox.safaricom.co.ke/mpesa/c2b/v1/registerurl" # "http://sandbox.safaricom.co.ke/mpesa/c2b/v1/registerurl"
    headers = {"Authorization": "Bearer %s" % access_token}
    saf_request = { "ShortCode": "600000", "ResponseType": "confirmed", "ConfirmationURL": "https://cod.ngrok.io/payment/confirmed/", "ValidationURL": "https://9d308b9b.ngrok.io/payment/validation/"}
    response = requests.post(api_url, json=saf_request, headers=headers,  timeout=(3.05, 6.05))
    return HttpResponse(response)

# payment validation
@csrf_exempt    
def payment_validation(request):
    # returns an object from a string representing a json object.
    data = json.loads(request.body)
    print(data)
    order_id = data["BillRefNumber"]
    amount = float(data["TransAmount"])
    mpesaid = data["TransID"]

    # https://stackoverflow.com/q/3090302
    order = None
    try:
        order = Order.objects.get(pk=order_id)
    except Exception as e:
        # https://stackoverflow.com/a/7791383
        print(e)

    if(order != None):
        if(order.paid == False):
            print("({} == {}) => {}".format(order.get_total_cost(), amount, (order.get_total_cost()== amount)))
            if(order.get_total_cost() == amount):
                order.paid = True
                order.Mpesa_transid = mpesaid 
                order.save()
                return JsonResponse({"ResultCode": 0,"ResultDesc": "The service was accepted successfully"})
            else:
                return JsonResponse({"ResultCode": 0,"ResultDesc": "AMOUNT PAID NOT EQUAL TO ORDER TOTAL COST..."})
        else:
            return JsonResponse({"ResultCode": 0,"ResultDesc": "ORDER ALREADY PAID..."})
    else:
        return JsonResponse({"ResultCode": 0,"ResultDesc": "NO ORDER WITH ID :=> {}...".format(order_id)})


@csrf_exempt
def payment_confirmed(request):
    response = request.body
    # returns an object from a string representing a json object.
    data = json.loads(response)
    order_id = data["BillRefNumber"]
    amount = float(data["TransAmount"])
    mpesaid = data["TransID"]

    # https://stackoverflow.com/q/3090302
    order = None
    try:
        order = Order.objects.get(pk=order_id)
    except Exception as e:
        # https://stackoverflow.com/a/7791383
        print(e)

    if(order != None):
        if(order.paid == False):
            print("({} == {}) => {}".format(order.get_total_cost(), amount, (order.get_total_cost()== amount)))
            if(order.get_total_cost() == amount):
                order.paid = True
                order.Mpesa_transid = mpesaid 
                order.save()
                print("SAVED ORDER AS PAID...")
            else:
                print("AMOUNT PAID NOT EQUAL TO ORDER TOTAL COST...")
        else:
            print("ORDER ALREADY PAID...")
    else:
        print("NO ORDER WITH ID :=> {}...".format(order_id))

    return JsonResponse({"ResultCode": 0,"ResultDesc": "The service was accepted successfully"})




#simulating transaction
def saf_simulation(request):
	host_name = "https://6ec449ce.ngrok.io"
	access_token = safaricom_access_token()
	api_url = "https://sandbox.safaricom.co.ke/mpesa/c2b/v1/simulate"
	headers = {"Authorization": "Bearer %s" % access_token}
	request = { 
		"ShortCode":"600000",
  		"CommandID":"CustomerPayBillOnline",
  		"Amount":"5000",
  		"Msisdn":"254708374149",
  		"BillRefNumber":"78" 
  		}
	response = requests.post(api_url, json = request, headers=headers)
	return HttpResponse(response) 


