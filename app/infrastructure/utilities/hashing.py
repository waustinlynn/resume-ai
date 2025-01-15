import hashlib
import hmac


def hash_value(value: str, secret: str) -> str:
    """
    Hash a value with a secret using HMAC and SHA256.

    Args:
        value (str): The value to hash.
        secret (str): The secret key used for hashing.

    Returns:
        str: The resulting hash in hexadecimal format.
    """
    # Encode the value and secret to bytes
    value_bytes = value.encode("utf-8")
    secret_bytes = secret.encode("utf-8")

    # Create an HMAC object
    hmac_obj = hmac.new(secret_bytes, value_bytes, hashlib.sha256)

    # Return the hash in hexadecimal format
    return hmac_obj.hexdigest()
