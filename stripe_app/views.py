from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from abstractbaseuser_project import settings
from rest_framework import status
import stripe


class PaymentView(APIView):
    def post(self, request):
        print('------------ came here ----------------')
        stripe.api_key = settings.STRIPE_SECRET_KEY
        intent = stripe.PaymentIntent.create(
            amount="100",
            currency="usd",
            automatic_payment_methods={"enabled": True},
        )
        print(intent, '---------------------intetn------------')
        return Response(data={
            'tax': "1",
            'client_secret': intent.client_secret
        }, status=status.HTTP_201_CREATED)
