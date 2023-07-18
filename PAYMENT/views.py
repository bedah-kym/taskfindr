from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from django_daraja.mpesa.core import MpesaClient
import json

def index(request):
    cl = MpesaClient()
    # Use a Safaricom phone number that you have access to, for you to be able to view the prompt.
    phone_number = '0748677515'
    amount = 1
    account_reference = 'reference'
    transaction_desc = 'Description'
    callback_url = 'https://sandbox.safaricom.co.ke/mpesa/c2b/v1/registerurl'
    response = cl.stk_push(phone_number, amount, account_reference, transaction_desc, callback_url)
    if response["ResponseDescription"] == "Success. Request accepted for processing":
        print("redirecting to profile................")
    else:
        print("back to payment ")
    return HttpResponse(response)
    

def callbackhandler(request):
    data = json.loads(request.body)
    if request.method == 'POST':
        data = json.loads(request.body)
        print(data)
        
        # Extract information from the JSON data
        
        
        # Perform operations on the extracted data
        
        # Return a JSON response
    else:
        pass

    return JsonResponse(data)