import logging
import requests
import hmac

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def make_request(**kwargs):
    try:
        req = requests.request(**kwargs)
    except Exception as e:
        logger.exception("Request Error: {}".format(str(e)))
        return None
    else:
        return req


def hash_hmac(secret_key, string, digest):
    """Create signature"""
    string_to_sign = string.encode('utf-8')
    hashed = hmac.HMAC(
        secret_key, string_to_sign, digest).hexdigest()
    return hashed

