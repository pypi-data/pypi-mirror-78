from django.conf import settings
from .models import MomoTransaction
import string, random, json, requests, hashlib
from .enum import NetworkTypes, StatusTypes
from django.core.serializers.json import DjangoJSONEncoder 

class MomoPayProcessor:
    
    def __init__(self, data=None, merchant={}, callback=None, *args, **kwargs):

        if data is not None:
            self.user = data['user']
            self.amount = data['amount']
            self.momo_number = data['customerNumber']
            self.network = data['payby']
            self.item_desc = data['item_desc']
            self.orderID = data.get('order_id', self.generateOrderID())
            self.network_name = NetworkTypes(data['payby']).name
        
        if callback is not None:
            self.callback = callback
        
        self.merchantID = merchant.get('id', settings.PAYMENT_MERCHANT)
        self.merchant_username = merchant.get('username', settings.PAYMENT_USERNAME)
        self.merchant_password = merchant.get('password', settings.PAYMENT_PASSWORD)

    def pay(self):

        self.getPaymentPayload()
        
        self.momotrans = MomoTransaction.objects.create(
            user = self.user,
            amount = self.amount,
            network = self.network,
            msisdn = self.momo_number,
            info_sent = self.payload,
            order_id = self.orderID,
            merchant_id = self.merchantID,
            merchant_name = self.merchant_username,
        )
        self.response = requests.post(settings.PAYMENT_GATEWAY, data=json.dumps(self.payload, cls=DjangoJSONEncoder))
        self.momotrans.initial_callback = self.response.text
        self.momotrans.save()
        self.parseMomoResponse()

        

    def parseMomoResponse(self):

        try:
            response = self.response.json()
            
            if response["Status"] == "Accepted":
                self.momotrans.ext_id = response["InvoiceNo"]
                self.momotrans.save()
                return {"status":True, "message":"Passed"}

            self.momotrans.final_callback = response.text
            
        except Exception as e:
            # print(e)
            self.momotrans.final_callback = f"{e}"
        
        self.momotrans.status = StatusTypes.FAILED
        self.momotrans.save()
        return {"status": False, "message":"Failed"}


    
    def generateOrderID(self):
        alphabet = string.ascii_uppercase + string.digits
        return ''.join(random.choices(alphabet, k=12))


    def getPaymentPayload(self):
        key = random.randint(1000, 9999)
        secret = hashlib.md5((self.merchant_username+str(key)+self.merchant_password).encode("utf-8")).hexdigest()
        self.payload = {
            'merchant_id': self.merchantID,
            'secrete': secret,
            'key': key,
            'item_desc': self.item_desc,
            'callback': settings.PAYMENT_CALLBACK,
            'order_id': self.orderID,
            'customerName': self.user.username,
            'customerNumber': self.momo_number,
            'payby': self.network_name,
            'amount': self.amount,
        }
        if self.network == NetworkTypes.VODAFONE:
            self.payload["newVodaPayment"] = True



    def onCallback(self):
        if self.callback is not None:
        
            if self.callback["Status"] == "PAID":
                self.status_type = StatusTypes.COMPLETED
            else:
                self.status_type = StatusTypes.FAILED

            try:
                momo_trans = MomoTransaction.objects.get(
                    order_id=self.callback["Order_id"],
                    ext_id=self.callback["InvoiceNo"])
                momo_trans.final_callback = json.dumps(self.callback , cls=DjangoJSONEncoder)
                momo_trans.status = self.status_type                
                momo_trans.save()
                return {"status":True, "transactionID":momo_trans.id, "amount":momo_trans.amount}
            except Exception as e:
                return {"status":False, "message":f"{e}"}