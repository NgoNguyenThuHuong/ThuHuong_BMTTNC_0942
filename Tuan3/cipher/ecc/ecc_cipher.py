import ecdsa
import os


KEY_DIR = "cipher/ecc/keys"

if not os.path.exists(KEY_DIR):
    os.makedirs(KEY_DIR)


class ECCCipher:

    def __init__(self):
        pass

    def generate_keys(self):
        """Sinh cặp khóa ECC"""

        sk = ecdsa.SigningKey.generate()
        vk = sk.get_verifying_key()

        with open(f"{KEY_DIR}/privateKey.pem", "wb") as f:
            f.write(sk.to_pem())

        with open(f"{KEY_DIR}/publicKey.pem", "wb") as f:
            f.write(vk.to_pem())

        return True

    def load_keys(self):
        """Đọc khóa từ file"""

        with open(f"{KEY_DIR}/privateKey.pem", "rb") as f:
            private_key = ecdsa.SigningKey.from_pem(f.read())

        with open(f"{KEY_DIR}/publicKey.pem", "rb") as f:
            public_key = ecdsa.VerifyingKey.from_pem(f.read())

        return {
            "private_key": private_key,
            "public_key": public_key
        }

    def sign(self, message, private_key):
        """Ký dữ liệu"""

        if not message:
            raise ValueError("Message is empty")

        signature = private_key.sign(
            message.encode("utf-8")
        )

        return signature

    def verify(self, message, signature, public_key):
        """Kiểm tra chữ ký"""

        try:
            return public_key.verify(
                signature,
                message.encode("utf-8")
            )

        except ecdsa.BadSignatureError:
            return False


if __name__ == "__main__":

    print("=== ECC TEST ===")

    ecc = ECCCipher()

    print("Generating keys...")
    ecc.generate_keys()

    keys = ecc.load_keys()

    message = "Hello ECC"

    print("Message:", message)

    signature = ecc.sign(
        message,
        keys["private_key"]
    )

    print("Signature:")
    print(signature.hex())

    result = ecc.verify(
        message,
        signature,
        keys["public_key"]
    )

    print("Verify:", result)