from collections import OrderedDict
from unittest.mock import MagicMock
from tests.base import BaseTest


class TestCardPayment(BaseTest):
    def test_payment_status(self):
        kwargs = OrderedDict()
        kwargs["oid"] = self.order_id
        kwargs["vid"] = self.vid
        data = {
            "header_status": 200,
            "status": 1,
            "text": "payment record found",
            "data": {
                "vid": self.vid,
                "session_id": self.sid,
                "oid": self.order_id,
                "transaction_amount": self.amount,
                "transaction_code": "TXNCODE",
                "telephone": "2547XXXXXXXX",
                "firstname": "JOHN",
                "lastname": "DOE",
                "paid_at": "2016-05-14 16:13:50",
                "payment_mode": "MPESA"
            },
            "hash": "d29ac43a8b89673cc85ce206351832d3a0c4a462dd0fde56c17445e94f6ad958"
        }
        self.instance.payment_status_request = MagicMock(
            return_value=data)
        response = self.instance.payment_status_request(kwargs)
        assert response["status"] == 1
