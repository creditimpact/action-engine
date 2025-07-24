import os
import base64
import subprocess

_KEY = os.getenv("VAULT_ENCRYPTION_KEY", "0" * 32).encode()
_IV = os.getenv("VAULT_ENCRYPTION_IV", "1" * 16).encode()


def _hex(b: bytes) -> str:
    return b.hex()


def encrypt(text: str) -> str:
    """Encrypt ``text`` using AES-256-CBC via OpenSSL."""
    result = subprocess.run(
        [
            "openssl",
            "enc",
            "-aes-256-cbc",
            "-base64",
            "-A",
            "-K",
            _hex(_KEY),
            "-iv",
            _hex(_IV),
            "-nosalt",
        ],
        input=text.encode(),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=True,
    )
    return result.stdout.decode()


def decrypt(token: str) -> str:
    """Decrypt token produced by :func:`encrypt`."""
    result = subprocess.run(
        [
            "openssl",
            "enc",
            "-d",
            "-aes-256-cbc",
            "-base64",
            "-A",
            "-K",
            _hex(_KEY),
            "-iv",
            _hex(_IV),
            "-nosalt",
        ],
        input=token.encode(),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=True,
    )
    return result.stdout.decode()
