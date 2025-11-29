from cryptography.fernet import Fernet


def generate_aes_key() -> str:
    """
    Generates a new AES key (URL-safe base64 encoded).
    Store this securely. Do NOT regenerate it on every request.
    """
    return Fernet.generate_key().decode("utf-8")


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