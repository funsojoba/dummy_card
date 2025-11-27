import uuid
import string
import hmac, hashlib, base64



def generate_id():
    return uuid.uuid4().hex


def generate_otp():
    return string



def generate_hmac_signature(secret, payload):
    msg = json.dumps(payload).encode()
    hashed = hmac.new(secret.encode(), msg, hashlib.sha256).digest()
    return base64.b64encode(hashed).decode()