import cryptography
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
class Encryption:
    def __init__(self):
        self.private_key = ""
        self.public_key = ""
        self.private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
            backend=default_backend()
        )
        self.public_key = self.private_key.public_key()
        

    
    def encrypt_message(self, message):
        encrypted = self.public_key.encrypt(
            message,
            padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        return encrypted

    def decrypt_message(self, message):
   
        original_message = self.private_key.decrypt(
            message,
            padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )

        return original_message.decode("utf-8")