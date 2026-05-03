import binascii
import hashlib
import hmac
import os

from sources.config import HASH_NAME, ITERATIONS, SALT_SIZE


# -----------------------------
# Password hashing
# -----------------------------
def hash_password(password: str) -> str:
    salt = os.urandom(SALT_SIZE)
    dk = hashlib.pbkdf2_hmac(
        HASH_NAME,
        password.encode("utf-8"),
        salt,
        ITERATIONS
    )

    salt_hex = binascii.hexlify(salt).decode()
    dk_hex = binascii.hexlify(dk).decode()

    return (
        f"{HASH_NAME}$"
        f"{ITERATIONS}$"
        f"{salt_hex}$"
        f"{dk_hex}"
    )


def verify_password(stored: str, password: str) -> bool:
    hash_name, iters, salt_hex, dk_hex = stored.split("$")
    salt = binascii.unhexlify(salt_hex)
    expected = binascii.unhexlify(dk_hex)

    dk = hashlib.pbkdf2_hmac(
        hash_name,
        password.encode("utf-8"),
        salt,
        int(iters)
    )

    return hmac.compare_digest(dk, expected)