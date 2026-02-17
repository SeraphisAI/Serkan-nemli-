from abc import ABC, abstractmethod


class KEMAdapter(ABC):
    @abstractmethod
    def encapsulate(self, public_key: bytes) -> tuple[bytes, bytes]:
        raise NotImplementedError

    @abstractmethod
    def decapsulate(self, secret_key: bytes, ciphertext: bytes) -> bytes:
        raise NotImplementedError


class DSASignatureAdapter(ABC):
    @abstractmethod
    def sign(self, message: bytes, private_key: bytes) -> bytes:
        raise NotImplementedError

    @abstractmethod
    def verify(self, message: bytes, signature: bytes, public_key: bytes) -> bool:
        raise NotImplementedError


class StubPQCAdapter(KEMAdapter, DSASignatureAdapter):
    def encapsulate(self, public_key: bytes) -> tuple[bytes, bytes]:
        return b"stub-ciphertext", b"stub-shared-secret"

    def decapsulate(self, secret_key: bytes, ciphertext: bytes) -> bytes:
        return b"stub-shared-secret"

    def sign(self, message: bytes, private_key: bytes) -> bytes:
        return b"stub-signature"

    def verify(self, message: bytes, signature: bytes, public_key: bytes) -> bool:
        return signature == b"stub-signature"
