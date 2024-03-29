
from rest_framework.serializers import ValidationError
from rest_framework import status
import razorpay
from django.conf import settings


client = razorpay.Client(auth=(
    settings.RAZORPAY_PUBLIC_KEY,
    settings.RAZORPAY_SECRET_KEY
    )
)

class RazorpayClient:
    def create_order(self, amount, currency):
        data = {
            "amount": amount * 100,
            "currency": currency,
        }
        try:
            self.order = client.order.create(data=data)
            return self.order
        except Exception as e:
            raise ValidationError(
                {
                    "status_code": status.HTTP_400_BAD_REQUEST,
                    "message": e
                }
            )
    
    def verify_payment_signature(self, razorpay_order_id, razorpay_payment_id, razorpay_signature):
        try:
            self.verify_signature = client.utility.verify_payment_signature({
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': razorpay_payment_id,
                'razorpay_signature': razorpay_signature
            })
            return self.verify_signature
        except Exception as e:
            raise ValidationError(
                {
                    "error": e,
                    "message": "please check razorpay_order_id,razorpay_payment_id,razorpay_signature",
                    "status_code": status.HTTP_400_BAD_REQUEST
                }
            )
            