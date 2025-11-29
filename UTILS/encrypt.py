from cryptography.fernet import Fernet
import base64
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.hkdf import HKDF


def generate_aes_key() -> str:
    """
    Generates a new AES key (URL-safe base64 encoded).
    Store this securely. Do NOT regenerate it on every request.
    """
    return Fernet.generate_key().decode("utf-8")


def derive_fernet_key(org_id: str, master_secret: str) -> str:
    """
    Derive a per-organization Fernet key from org_id + master_secret.
    Returns a URL-safe base64-encoded 32-byte key suitable for Fernet.
    """
    # Use HKDF to derive a fixed 32-byte key
    hkdf = HKDF(
        algorithm=hashes.SHA256(),
        length=32,
        salt=None,             # optional: can use per-org salt
        info=b"webhook-secret",
    )
    raw_key = hkdf.derive(f"{org_id}{master_secret}".encode())

    # Fernet requires URL-safe base64-encoded 32-byte key
    fernet_key = base64.urlsafe_b64encode(raw_key).decode()
    return fernet_key

def encrypt_string(key: str, raw_text: str) -> str:
    """
    Encrypt a string using AES (Fernet).
    Returns encrypted text as a URL-safe base64 string.
    """
    if raw_text is None:
        raise ValueError("raw_text cannot be None")

    f = Fernet(key.encode("utf-8"))
    encrypted = f.encrypt(raw_text.encode("utf-8"))
    return encrypted.decode("utf-8")


def decrypt_string(key: str, encrypted_text: str) -> str:
    """
    Decrypt an AES-encrypted string.
    Returns the original plaintext.
    """
    f = Fernet(key.encode("utf-8"))
    decrypted = f.decrypt(encrypted_text.encode("utf-8"))
    return decrypted.decode("utf-8")