import rsa
import os

class RSACipher:
    def __init__(self, key_dir="."):
        self.key_dir = key_dir
        self.public_key_path = os.path.join(self.key_dir, 'public.pem')
        self.private_key_path = os.path.join(self.key_dir, 'private.pem')

    def generate_keys(self):
        (public_key, private_key) = rsa.newkeys(1024)
        
        with open(self.public_key_path, 'wb') as f:
            f.write(public_key.save_pkcs1())
            
        with open(self.private_key_path, 'wb') as f:
            f.write(private_key.save_pkcs1())

    def load_keys(self):
        try:
            with open(self.public_key_path, 'rb') as f:
                pub_data = f.read()
                public_key = rsa.PublicKey.load_pkcs1(pub_data)
                
            with open(self.private_key_path, 'rb') as f:
                priv_data = f.read()
                private_key = rsa.PrivateKey.load_pkcs1(priv_data)
                
            return private_key, public_key
            
        except FileNotFoundError:
            self.generate_keys()
            return self.load_keys()

    def encrypt(self, message, key):
        if isinstance(message, str):
            message = message.encode('utf-8')
        return rsa.encrypt(message, key)

    def decrypt(self, ciphertext, key):
        return rsa.decrypt(ciphertext, key)

    def sign(self, message, key):
        if isinstance(message, str):
            message = message.encode('utf-8')
        return rsa.sign(message, key, 'SHA-256')

    def verify(self, message, signature, key):
        if isinstance(message, str):
            message = message.encode('utf-8')
        try:
            rsa.verify(message, signature, key)
            return True
        except rsa.VerificationError:
            return False
