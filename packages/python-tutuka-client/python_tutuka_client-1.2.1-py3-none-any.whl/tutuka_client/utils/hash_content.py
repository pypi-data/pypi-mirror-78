from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes, hmac


def hmac_with_sha1(password: bytes, string: bytes):
    hash_result = hmac.HMAC(
        password,
        algorithm=hashes.SHA1(),  # noqa: S303
        backend=default_backend(),
    )
    hash_result.update(string)
    return hash_result.finalize().hex().upper()
