from collections import OrderedDict
from ipay_sdk.gateway import Ipay


class BaseTest:
    @classmethod
    def setup_class(cls):
        cls.hash_key = "demoCHANGED"
        cls.vid = "demo"
        cls.order_id = "573737373673"
        cls.amount = 10
        cls.test_number = "000000000000"
        cls.test_email = "write2sartim@gmail.com"
        cls.instance = Ipay(cls.hash_key)
        cls.callback_url = "https://path/to/callback"
        cls.currency = "KES"
        kwargs = OrderedDict()
        kwargs["live"] = 0
        kwargs["oid"] = cls.order_id
        kwargs["inv"] = cls.order_id
        kwargs["amount"] = cls.amount
        kwargs["tel"] = cls.test_number
        kwargs["eml"] = cls.test_email
        kwargs["vid"] = cls.vid
        kwargs["curr"] = cls.currency
        kwargs["p1"] = "0"
        kwargs["p2"] = "123"
        kwargs["p3"] = "456"
        kwargs["p4"] = "789"
        kwargs["cst"] = 1
        kwargs["cbk"] = cls.callback_url
        response = cls.instance.initiator_request(kwargs)
        assert response["header_status"] == 200
        assert response["status"] == 1
        cls.sid = response["data"]["sid"]
