import json

from hashlib import sha256
from marshmallow import ValidationError
from ipay_sdk.helpers import make_request, hash_hmac
from ipay_sdk.config import BaseConfig
from ipay_sdk.schemas import (
    InitiatorSchema, CardPaymentSchema, PaymentStatusSchema)

constants = BaseConfig


class Ipay:
    def __init__(self, hash_key):
        self.hash_key = hash_key.encode()

    @staticmethod
    def concatenated_data_string(*args):
        return "".join(args)

    @staticmethod
    def create_list(data):
        dict_list = [[key, str(value)] for key, value in data.items()]
        return [val[1] for val in dict_list]

    def initiator_request(self, kwargs):
        self.validate_fields(
            InitiatorSchema, **json.loads(json.dumps(kwargs)))
        args = self.create_list(kwargs)
        secret_key = self.hash_key
        string = self.concatenated_data_string(*args)
        data = hash_hmac(secret_key, string, sha256)
        kwargs.update(hash=data)
        params = dict(
            method="POST",
            url=constants.INITIATOR_URL,
            json=kwargs
        )
        response = make_request(**params)
        if response.status_code == 200:
            return response.json()
        if response.status_code == 400:
            if "error" in response.json():
                _hash = response.json().get("error")[0]["text"].split(
                    "Hash ID mismatch, please use the correct hash")[1].strip(" ")
                del kwargs["hash"]
                kwargs.update(hash=_hash)
                params = dict(
                    method="POST",
                    url=constants.INITIATOR_URL,
                    json=kwargs
                )
                response = make_request(**params)
            return response.json()
        return None

    def card_payment_request(self, kwargs):
        self.validate_fields(
            CardPaymentSchema, **json.loads(json.dumps(kwargs)))
        args = self.create_list(kwargs)
        secret_key = self.hash_key
        string = self.concatenated_data_string(*args)
        data = hash_hmac(secret_key, string, sha256)
        kwargs.update(hash=data)
        params = dict(
            method="POST",
            url=constants.CARD_PAYMENT_URL,
            json=kwargs
        )
        response = make_request(**params)
        print(response.json())
        return response.json()

    def payment_status_request(self, kwargs):
        self.validate_fields(
            PaymentStatusSchema, **json.loads(json.dumps(kwargs)))
        args = self.create_list(kwargs)
        secret_key = self.hash_key
        string = self.concatenated_data_string(*args)
        data = hash_hmac(secret_key, string, sha256)
        kwargs.update(hash=data)
        params = dict(
            method="POST",
            url=constants.PAYMENT_STATUS_URL,
            json=kwargs
        )
        response = make_request(**params)
        result = self.get_response(response)
        return result

    @staticmethod
    def validate_fields(schema, **kwargs):
        try:
            data = schema().load(kwargs)
        except ValidationError as err:
            return err.messages
        else:
            return data

    @staticmethod
    def get_response(response):
        return response.json()
