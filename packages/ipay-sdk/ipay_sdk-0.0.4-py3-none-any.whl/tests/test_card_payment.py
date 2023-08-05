from collections import OrderedDict
from unittest.mock import MagicMock
from tests.base import BaseTest


class TestCardPayment(BaseTest):
    def test_card_payment(self):
        kwargs = OrderedDict()
        kwargs["sid"] = self.sid
        kwargs["vid"] = self.vid
        kwargs["cardno"] = "1234567895847543"
        kwargs["cvv"] = "123"
        kwargs["month"] = "12"
        kwargs["year"] = "2020"
        kwargs["cust_address"] = "Billing, Address"
        kwargs["cust_city"] = "City"
        kwargs["cust_country"] = "Country"
        kwargs["cust_postcode"] = "0000"
        kwargs["cust_stateprov"] = "State/Province"
        kwargs["fname"] = "fname"
        kwargs["lname"] = "lname"
        data = {
            "txncd": "1111111122", "qwh": "1000988633", "afd": "827071654",
            "poi": "1211883119", "uyt": "1431931896", "ifd": "548464895",
            "agt": "", "id": self.order_id, "status": "bdi6p2yy76etrs",
            "ivm": "oid", "mc": "100", "p1": "", "p2": "", "p3": "", "p4": "",
            "msisdn_id": "John Doe", "msisdn_idnum": "123456",
            "msisdn_custnum": "123456", "channel": "Credit_Card",
            "card_mask": "444444xxxxxx4444"}
        self.instance.card_payment_request = MagicMock(
            return_value=data)
        response = self.instance.card_payment_request(kwargs)
        assert response["id"] == self.order_id
