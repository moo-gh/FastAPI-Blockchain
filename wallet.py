import binascii
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import serialization, hashes


class Wallet:
    def __init__(self):
        self.private_key = ec.generate_private_key(ec.SECP256K1())
        self.public_key = self.private_key.public_key()

    def get_private_key(self) -> str:
        """Returns the private key in hex format"""
        private_bytes = self.private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption(),
        )
        return binascii.hexlify(private_bytes).decode("utf-8")

    def get_public_key(self) -> str:
        """Returns the public key in hex format (used as the address)"""
        public_bytes = self.public_key.public_bytes(
            encoding=serialization.Encoding.X962,
            format=serialization.PublicFormat.UncompressedPoint,
        )
        return binascii.hexlify(public_bytes).decode("utf-8")

    @staticmethod
    def sign_transaction(private_key_pem: str, transaction_data: str) -> str:
        """Signs transaction data with the private key"""
        private_bytes = binascii.unhexlify(private_key_pem)
        private_key = serialization.load_pem_private_key(
            private_bytes,
            password=None,
        )
        signature = private_key.sign(
            transaction_data.encode("utf-8"),
            ec.ECDSA(hashes.SHA256())
        )
        return binascii.hexlify(signature).decode("utf-8")

    @staticmethod
    def verify_signature(public_key_hex: str, signature_hex: str, transaction_data: str) -> bool:
        """Verifies a transaction signature"""
        try:
            public_bytes = binascii.unhexlify(public_key_hex)
            public_key = ec.EllipticCurvePublicKey.from_encoded_point(
                ec.SECP256K1(),
                public_bytes
            )
            signature = binascii.unhexlify(signature_hex)
            public_key.verify(
                signature,
                transaction_data.encode("utf-8"),
                ec.ECDSA(hashes.SHA256())
            )
            return True
        except Exception:
            return False

