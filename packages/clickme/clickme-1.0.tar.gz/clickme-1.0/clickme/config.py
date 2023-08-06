import hashlib
import datetime
from django.conf import settings

from clickme.methods import *


class Config():
    URL = settings.CLICKME_SETTINGS['ENDPOINT']
    CARD_CREATE_URL = URL + CARD_CREATE
    CARD_VERIFY_URL = URL + CARD_VERIFY
    PAYMENT_URL = URL + PAYMENT
    SERVICE_ID = settings.CLICKME_SETTINGS['SERVICE_ID']
    MERCHANT_USER_ID = settings.CLICKME_SETTINGS['MERCHANT_USER_ID']
    SECRET_KEY = settings.CLICKME_SETTINGS['SECRET_KEY']

    def __init__(self):
        self.HEADER = self.auth()

    def auth(self):
        timestamp = int(datetime.datetime.now().timestamp())
        encoder = '{}{}'.format(timestamp, self.SECRET_KEY)
        digest = hashlib.sha1(encoder.encode('utf-8')).hexdigest()
        header = {'Auth':'{}:{}:{}'.format(self.MERCHANT_USER_ID, digest, timestamp)}
        return header