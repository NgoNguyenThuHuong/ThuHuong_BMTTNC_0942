# -*- coding: utf-8 -*-
from flask import Flask, request, jsonify
from cipher.rsa import RSACipher
from cipher.ecc.ecc_cipher import ECCCipher
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5 as Cipher_PKCS1
from Crypto.Signature import PKCS1_v1_5 as Signature_PKCS1
from Crypto.Hash import SHA256
import binascii


app = Flask(__name__)

# Đường dẫn lưu khóa RSA
PRIVATE_KEY_PATH = "private.pem"
PUBLIC_KEY_PATH = "public.pem"

def get_keys():
    try:
        with open(PRIVATE_KEY_PATH, "rb") as f:
            private_key = RSA.import_key(f.read())
        with open(PUBLIC_KEY_PATH, "rb") as f:
            public_key = RSA.import_key(f.read())
        return private_key, public_key
    except FileNotFoundError:
        return None, None

@app.route('/api/rsa/generate_keys', methods=['GET'])
def generate_keys():
    key = RSA.generate(2048)
    private_key = key.export_key()
    public_key = key.publickey().export_key()
    
    with open(PRIVATE_KEY_PATH, "wb") as f:
        f.write(private_key)
    with open(PUBLIC_KEY_PATH, "wb") as f:
        f.write(public_key)
        
    return jsonify({"message": "Sinh cặp khóa thành công và đã lưu vào file!"})

@app.route('/api/rsa/encrypt', methods=['POST'])
def encrypt():
    data = request.json
    message = data.get("message", "")
    if not message:
        return jsonify({"error": "Message rỗng"}), 400
        
    _, public_key = get_keys()
    if not public_key:
        return jsonify({"error": "Chưa sinh khóa"}), 400
        
    cipher = Cipher_PKCS1.new(public_key)
    ciphertext = cipher.encrypt(message.encode('utf-8'))
    hex_ciphertext = binascii.hexlify(ciphertext).decode('utf-8')
    return jsonify({"encrypted_message": hex_ciphertext})

@app.route('/api/rsa/decrypt', methods=['POST'])
def decrypt():
    data = request.json
    ciphertext_hex = data.get("ciphertext", "")
    if not ciphertext_hex:
        return jsonify({"error": "Ciphertext rỗng"}), 400
        
    private_key, _ = get_keys()
    if not private_key:
        return jsonify({"error": "Chưa sinh khóa"}), 400
        
    try:
        ciphertext = binascii.unhexlify(ciphertext_hex.strip())
        cipher = Cipher_PKCS1.new(private_key)
        sentinel = b"Loi giai ma"
        decrypted_bytes = cipher.decrypt(ciphertext, sentinel)
        return jsonify({"decrypted_message": decrypted_bytes.decode('utf-8')})
    except Exception as e:
        return jsonify({"error": f"Lỗi xử lý dữ liệu: {str(e)}"}), 500

@app.route('/api/rsa/sign', methods=['POST'])
def sign():
    data = request.json
    message = data.get("message", "")
    if not message:
        return jsonify({"error": "Message rỗng"}), 400
        
    private_key, _ = get_keys()
    if not private_key:
        return jsonify({"error": "Chưa sinh khóa"}), 400
        
    try:
        h = SHA256.new(message.encode('utf-8'))
        signer = Signature_PKCS1.new(private_key)
        signature = signer.sign(h)
        hex_signature = binascii.hexlify(signature).decode('utf-8')
        return jsonify({"signature": hex_signature})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/rsa/verify', methods=['POST'])
def verify():
    data = request.json
    message = data.get("message", "")
    signature_hex = data.get("signature", "")
    if not message or not signature_hex:
        return jsonify({"error": "Thiếu message hoặc chữ ký"}), 400
        
    _, public_key = get_keys()
    if not public_key:
        return jsonify({"error": "Chưa sinh khóa"}), 400
        
    try:
        signature = binascii.unhexlify(signature_hex.strip())
        h = SHA256.new(message.encode('utf-8'))
        verifier = Signature_PKCS1.new(public_key)
        is_verified = verifier.verify(h, signature)
        return jsonify({"is_verified": is_verified})
    except Exception:
        return jsonify({"is_verified": False})

# ECC CIPHER ALGORITHM
ecc_cipher = ECCCipher()

@app.route('/api/ecc/generate_keys', methods=['GET'])
def ecc_generate_keys():
    ecc_cipher.generate_keys()
    return jsonify({'message': 'Keys generated successfully'})

@app.route('/api/ecc/sign', methods=['POST'])
def ecc_sign_message():
    data = request.json
    message = data['message']
    private_key, _ = ecc_cipher.load_keys()
    signature = ecc_cipher.sign(message, private_key)
    signature_hex = signature.hex()
    return jsonify({'signature': signature_hex})

@app.route('/api/ecc/verify', methods=['POST'])
def ecc_verify_signature():
    data = request.json
    message = data['message']
    signature_hex = data['signature']
    public_key, _ = ecc_cipher.load_keys()
    signature = bytes.fromhex(signature_hex)
    is_verified = ecc_cipher.verify(message, signature, public_key)
    return jsonify({'is_verified': is_verified})

if __name__ == '__main__':
    app.run(debug=True, port=5000)