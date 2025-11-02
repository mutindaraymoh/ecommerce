import requests
from django.shortcuts import render
from django.http import JsonResponse
from requests.auth import HTTPBasicAuth
import json
from django.http import HttpResponse
import base64
from django.contrib import messages
from datetime import datetime
from django.views.decorators.csrf import csrf_exempt
from store.views  import get_cart_total

# Replace these with your actual credentials
CONSUMER_KEY = "ao3m7ca1WTNnCOfXjKOqxJEISRmNPZiQq1GwQr9OG3goh4yh"
CONSUMER_SECRET = "1U1jffnQ5q8ApBAKdPlSgONdODDrnWnjs2Qi2iCdkscsdxCTA703fvmexQ6QX6k8"
PASSKEY = "bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919"
BUSINESS_SHORT_CODE = "174379"  # Test Paybill
CALLBACK_URL ="https://tangela-hesperideous-temeka.ngrok-free.dev/api/callback/"


def generate_access_token():
    url = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"
    response = requests.get(url, auth=HTTPBasicAuth(CONSUMER_KEY, CONSUMER_SECRET))
    access_token = response.json().get('access_token')
    return access_token

@csrf_exempt
def lipa_na_mpesa_online(request):
    if request.method == "POST":
        access_token = generate_access_token()
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        password = base64.b64encode((BUSINESS_SHORT_CODE + PASSKEY + timestamp).encode()).decode()

        phone_number = request.POST.get("number", "").strip()
        if not phone_number.startswith("254") or not phone_number.isdigit():
            return render(request, "cart.html", {
                "error": "Enter a valid phone number starting with 254"
            })

        total = get_cart_total(request)

        payload = {
            "BusinessShortCode": BUSINESS_SHORT_CODE,
            "Password": password,
            "Timestamp": timestamp,
            "TransactionType": "CustomerPayBillOnline",
            "Amount": int(total),
            "PartyA": int(phone_number),
            "PartyB": BUSINESS_SHORT_CODE,
            "PhoneNumber": int(phone_number),
            "CallBackURL": CALLBACK_URL,  # Still required!
            "AccountReference": "raymond jj",
            "TransactionDesc": "Payment for items in cart",
        }

        stk_url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
        headers = {"Authorization": f"Bearer {access_token}"}
        response = requests.post(stk_url, json=payload, headers=headers)
        res = response.json()

        # ✅ Check if STK push was initiated successfully
        if res.get("ResponseCode") == "0":
            message = "STK Push sent! Please check your phone to complete payment."
        else:
            message = f"Failed to send STK Push: {res.get('errorMessage', 'Unknown error')}"

        # ✅ Show message on the same cart page
        cart = request.session.get('cart', {})
        total = get_cart_total(request)
        return render(request, "cart.html", {
            "cart": cart,
            "total": total,
            "message": message
        })

    return render(request, "cart.html")


    
@csrf_exempt
def stk_callback(request):
    data = json.loads(request.body.decode('utf-8'))
    print("Callback Data:", data)

    # You can save the transaction result in your database here
    return HttpResponse("Callback received successfully")
