from __future__ import annotations

from cryptography.fernet import Fernet

from .config import get_settings


class SecretCipher:
    def __init__(self, fernet_key: str):
        if not fernet_key:
            raise RuntimeError("ENCRYPTION_FERNET_KEY is required.")
        self._fernet = Fernet(fernet_key.encode("utf-8"))

    def encrypt(self, plaintext: str) -> str:
        return self._fernet.encrypt(plaintext.encode("utf-8")).decode("utf-8")

    def decrypt(self, ciphertext: str) -> str:
        return self._fernet.decrypt(ciphertext.encode("utf-8")).decode("utf-8")


def get_cipher() -> SecretCipher:
    settings = get_settings()
    return SecretCipher(settings.encryption_fernet_key)
