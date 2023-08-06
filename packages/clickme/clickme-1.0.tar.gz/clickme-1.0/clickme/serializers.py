from rest_framework import serializers


class CardCreateSerializer(serializers.Serializer):
    card_number = serializers.CharField()
    expire_date = serializers.CharField()
    temporary = serializers.CharField()


class CardVerifySerializer(serializers.Serializer):
    trans_id = serializers.IntegerField()
    card_token = serializers.CharField()
    sms_code = serializers.IntegerField()


class PaymentSerializer(serializers.Serializer):
    card_token = serializers.CharField()
    amount = serializers.DecimalField(max_digits=10, decimal_places=2)
    order_id = serializers.IntegerField()
