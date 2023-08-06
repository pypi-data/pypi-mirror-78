import requests

from rest_framework.views import APIView
from rest_framework.response import Response

from clickme.serializers import *
from clickme.config import Config
from clickme.models import Transaction


class CardCreateApiView(APIView):
    def __init__(self):
        self.conf = Config()
        self.trans = Transaction()
        super(CardCreateApiView, self).__init__()

    def post(self, request):
        serializer = CardCreateSerializer(data=request.data, many=False)
        serializer.is_valid(raise_exception=True)
        result = self.card_create(serializer.validated_data)

        return Response(result)

    def card_create(self, validated_data):

        data = dict(
            service_id=self.conf.SERVICE_ID,
            card_number=validated_data['card_number'],
            expire_date=validated_data['expire_date'],
            temporary=validated_data['temporary'],
        )

        response = requests.post(self.conf.CARD_CREATE_URL, json=data, headers=self.conf.HEADER)
        result = response.json()
        if result['error_code'] != 200 and result['error_code'] != 201:
            trans = self.trans.create_transaction(
                error_code=result['error_code'],
                error_note=result['error_note'],
                status=self.trans.FAILED
            )
            result.update({
                'trans_id':trans.id
            })
        else:
            trans = self.trans.create_transaction(
                error_code=result['error_code'],
                error_note=result['error_note'],
                status=self.trans.PROCESS
            )
            result.update({
                'trans_id': trans.id
            })

        return result


class CardVerifyApiView(APIView):
    def __init__(self):
        self.conf = Config()
        self.trans = Transaction()
        super(CardVerifyApiView, self).__init__()

    def post(self, request):
        serializer = CardVerifySerializer(data=request.data, many=False)
        serializer.is_valid(raise_exception=True)
        result = self.card_verify(serializer.validated_data)

        return Response(result)

    def card_verify(self, validated_data):
        data = dict(
            service_id=self.conf.SERVICE_ID,
            card_token=validated_data['card_token'],
            sms_code=validated_data['sms_code'],
        )

        response = requests.post(self.conf.CARD_VERIFY_URL, json=data, headers=self.conf.HEADER)
        result = response.json()
        trans_id = validated_data['trans_id']
        trans = self.trans.objects.get(id=trans_id, status=self.trans.PROCESS)
        if result['error_code'] != 200:
            self.trans.update_transaction(
                trans=trans,
                status=self.trans.FAILED,
                error_code=result['error_code'],
                error_note=result['error_note']
            )

        else:
            self.trans.update_transaction(
                trans=trans,
                status=self.trans.VERIFY,
                error_code=result['error_code'],
                error_note=result['error_note']
            )
        result.update({
            'trans_id': trans.id
        })

        return result


class PaymentApiView(APIView):
    def __init__(self):
        self.conf = Config()
        self.trans = Transaction()
        super(PaymentApiView, self).__init__()

    def post(self, request):
        serializer = PaymentSerializer(data=request.data, many=False)
        serializer.is_valid(raise_exception=True)
        result = self.payment(serializer.validated_data)

        return Response(result)

    def payment(self, validated_data):
        data = dict(
            service_id=self.conf.SERVICE_ID,
            card_token=validated_data['card_token'],
            amount=validated_data['amount'],
            transaction_parameter=validated_data['order_id'],
        )

        response = requests.post(self.conf.PAYMENT_URL, json=data, headers=self.conf.HEADER)
        result = response.json()
        trans_id = validated_data['trans_id']
        trans = self.trans.objects.get(id=trans_id, status=self.trans.VERIFY)
        if result['error_code'] != 200:
            self.trans.update_transaction(
                trans=trans,
                status=self.trans.FAILED,
                error_code=result['error_code'],
                error_note=result['error_note']
            )

        else:
            self.trans.update_transaction(
                trans=trans,
                status=self.trans.PAID,
                error_code=result['error_code'],
                error_note=result['error_note'],
                payment_id=result['payment_id'],
                order_id=validated_data['order_id'],
                amount=validated_data['amount']
            )

        return result
