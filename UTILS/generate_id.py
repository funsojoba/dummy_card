import uuid
import bcrypt
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



def hash_string(raw: str) -> str:
    """
    Hash a string using bcrypt.
    Returns a UTF-8 decoded hash for database storage.
    """
    if raw is None:
        raise ValueError("String to hash cannot be None")

    hashed = bcrypt.hashpw(raw.encode("utf-8"), bcrypt.gensalt())
    return hashed.decode("utf-8")


def verify_hashed_string(raw: str, hashed: str) -> bool:
    """
    Compare a raw string with its bcrypt hashed value.
    Returns True if they match, False otherwise.
    """
    if raw is None or hashed is None:
        return False

    try:
        return bcrypt.checkpw(raw.encode("utf-8"), hashed.encode("utf-8"))
    except ValueError:
        return False