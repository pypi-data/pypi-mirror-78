from collections import OrderedDict
from tests.base import BaseTest


class TestGenerateCheckoutPage(BaseTest):
    def generate_checkout_page(self):
        kwargs = OrderedDict()
        kwargs["live"] = 0
        kwargs["oid"] = self.order_id
        kwargs["inv"] = self.order_id
        kwargs["ttl"] = self.amount
        kwargs["tel"] = self.test_number
        kwargs["eml"] = self.test_email
        kwargs["vid"] = self.vid
        kwargs["curr"] = self.currency
        kwargs["p1"] = "0"
        kwargs["p2"] = "123"
        kwargs["p3"] = "456"
        kwargs["p4"] = "789"
        kwargs["cbk"] = self.callback_url
        kwargs["cst"] = 1
        kwargs["crl"] = 0
        response = self.instance.process_request(kwargs)
        assert "html" in response
