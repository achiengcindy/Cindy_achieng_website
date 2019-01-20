from django.views import View
import requests, json
from requests.auth import HTTPBasicAuth
#https://devforgalaxy.github.io/en/2017/10/23/django-handle-json-request-en.html 
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404,redirect
from decimal import Decimal
from django.conf import settings
from orders.models import Order
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from cart.cart import Cart
   

""" To intergrate Mpesa api
1. generate tokens
2. register confirmation+ validation urls
3. simulate transaction """

#https://stackoverflow.com/questions/3630822/django-python-getting-field-name-from-database-get-object
# def payment_lipa(request, order_id):
#     order = get_object_or_404(Order,pk=order_id)
def payment_lipa(request, order_id):
    order = get_object_or_404(Order, pk=order_id)
    #print(order)
    #print(order.paid)
    if (order.paid == True):
        return render(request,'payment/lipa.html', {'order':order})
    else:
        return redirect('orders:order_created', order.id)
      
# generating acess tokens
def safaricom_access_token():
    try:
        consumer_key = settings.SAFARICOM_API_CONSUMER_KEY
        consumer_secret = settings.SAFARICOM_API_CONSUMER_SECRET
        api_URL = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"
        response = requests.get(api_URL, auth=HTTPBasicAuth(consumer_key, consumer_secret))
        return response.json()['access_token']
    except:
        return None

#send json data using python requests
# register confirmation and validation urls
@csrf_exempt
def saf_registration(request):
    #host = request.get_host()
    access_token = safaricom_access_token()
    api_url = "https://sandbox.safaricom.co.ke/mpesa/c2b/v1/registerurl"
    headers = {"Authorization": "Bearer %s" % access_token, 'Content-Type': 'application/json'}
    saf_request = {
        "ShortCode": "600000",
        "ResponseType": "confirmed",
        "ConfirmationURL": request.build_absolute_uri() + '/payment/confirmed/',
        "ValidationURL": request.build_absolute_uri() + '/payment/validation/'
    }
    print(saf_request)
    response = requests.post(api_url, json=saf_request, headers=headers,  timeout=(3.05, 6.05))
    return HttpResponse(response)


# payment validation 
def payment_validation(request): 
    #posting body of raw JSON request
    #request.body ia a  byte string,decode before passing it to load
    # body = request.body.decode('utf-8')
    body = request.body
    #read
    data = json.loads(body)
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
    return JsonResponse({"ResultCode": 0,"ResultDesc": "The service was accepted successfully"})

@csrf_exempt
def payment_confirmed(request):
    #decode 
    #body = request.body.decode('utf-8')
    #read
    data = json.loads(request.body)
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
                return JsonResponse({"ResultCode": 1,"ResultDesc": "AMOUNT PAID NOT EQUAL TO ORDER TOTAL COST..."})
                #print("AMOUNT PAID NOT EQUAL TO ORDER TOTAL COST...")
        else:
            return JsonResponse({"ResultCode": 1,"ResultDesc": "ORDER ALREADY PAID..."})
            #print("ORDER ALREADY PAID...")
    else:
        #print("NO ORDER WITH ID :=> {}...".format(order_id))
        return JsonResponse({"ResultCode": 1,"ResultDesc": "NO ORDER WITH ID :=> {}...".format(order_id)})
    return JsonResponse({"ResultCode": 0,"ResultDesc": "The service was accepted successfully"})
    #return  HttpResponse(json.dumps({ResultCode": 0,"ResultDesc": "The service was accepted successfully"}), content_type='application/json')

@csrf_exempt
#simulating transaction
def saf_simulation(request):
    host = request.get_host()
    print(host)
    access_token = safaricom_access_token()
    api_url = "https://sandbox.safaricom.co.ke/mpesa/c2b/v1/simulate"
    headers = {"Authorization": "Bearer %s" % access_token, 'Content-Type': 'application/json' } 
    request = { "ShortCode":"600000","CommandID":"CustomerPayBillOnline","Amount":"2000","Msisdn":"254708374149","BillRefNumber":"4" }
    response = requests.post(api_url, json = request, headers=headers)
    return JsonResponse(response.json()) 

