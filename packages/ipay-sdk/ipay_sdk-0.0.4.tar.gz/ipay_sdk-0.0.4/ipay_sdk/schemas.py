from marshmallow import Schema, fields


class CheckoutPageSchema(Schema):
    live = fields.Int(required=True)
    oid = fields.Str(required=True)
    inv = fields.Str(required=True)
    ttl = fields.Str(required=True)
    tel = fields.Str(required=True)
    eml = fields.Str(required=True)
    vid = fields.Str(required=True)
    curr = fields.Str(required=True)
    p1 = fields.Str(required=True)
    p2 = fields.Str(required=True)
    p3 = fields.Str(required=True)
    p4 = fields.Str(required=True)
    cbk = fields.Str(required=True)
    cst = fields.Int(required=True)
    crl = fields.Int(required=True)


class InitiatorSchema(Schema):
    live = fields.Int(required=True)
    oid = fields.Str(required=True)
    inv = fields.Str(required=True)
    amount = fields.Float(required=True)
    tel = fields.Str(required=True)
    eml = fields.Str(required=True)
    vid = fields.Str(required=True)
    curr = fields.Str(required=True)
    p1 = fields.Str(required=True)
    p2 = fields.Str(required=True)
    p3 = fields.Str(required=True)
    p4 = fields.Str(required=True)
    cbk = fields.Str(required=True)
    cst = fields.Int(required=True)


class CardPaymentSchema(Schema):
    sid = fields.Str(required=True)
    vid = fields.Str(required=True)
    curr = fields.Str(required=True)
    cardno = fields.Str(required=True)
    cvv = fields.Str(required=True)
    month = fields.Str(required=True)
    year = fields.Str(required=True)
    cust_address = fields.Str(required=True)
    cust_city = fields.Str(required=True)
    cust_country = fields.Str(required=True)
    cust_postcode = fields.Str(required=True)
    cust_stateprov = fields.Str(required=True)
    fname = fields.Str(required=True)
    lname = fields.Str(required=True)


class PaymentStatusSchema(Schema):
    oid = fields.Str(required=True)
    vid = fields.Str(required=True)
