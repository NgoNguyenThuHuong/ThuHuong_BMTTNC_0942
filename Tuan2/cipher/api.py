from flask import Flask, request, jsonify
from caesar import CaesarCipher
from vigenere import VigenereCipher
from railfence import RailFenceCipher
from playfair import PlayFairCipher
from transposition import TranspositionCipher

app = Flask(__name__)

# ================= CAESAR API =================
@app.route('/api/caesar/encrypt', methods=['POST'])
def caesar_encrypt():
    data = request.get_json()
    plain_text = data.get('plain_text')
    key = int(data.get('key'))
    cipher = CaesarCipher()
    encrypted_text = cipher.encrypt_text(plain_text, key)
    return jsonify({'encrypted_text': encrypted_text})

@app.route('/api/caesar/decrypt', methods=['POST'])
def caesar_decrypt():
    data = request.get_json()
    cipher_text = data.get('cipher_text')
    key = int(data.get('key'))
    cipher = CaesarCipher()
    decrypted_text = cipher.decrypt_text(cipher_text, key)
    return jsonify({'decrypted_text': decrypted_text})

# ================= VIGENERE API =================
@app.route('/api/vigenere/encrypt', methods=['POST'])
def vigenere_encrypt():
    data = request.get_json()
    plain_text = data.get('plain_text')
    key = data.get('key')
    cipher = VigenereCipher()
    encrypted_text = cipher.vigenere_encrypt(plain_text, key)
    return jsonify({'encrypted_text': encrypted_text})

@app.route('/api/vigenere/decrypt', methods=['POST'])
def vigenere_decrypt():
    data = request.get_json()
    cipher_text = data.get('cipher_text')
    key = data.get('key')
    cipher = VigenereCipher()
    decrypted_text = cipher.vigenere_decrypt(cipher_text, key)
    return jsonify({'decrypted_text': decrypted_text})

# ================= RAIL FENCE API =================
@app.route('/api/railfence/encrypt', methods=['POST'])
def railfence_encrypt():
    data = request.get_json()
    plain_text = data.get('plain_text')
    key = int(data.get('key'))
    cipher = RailFenceCipher()
    encrypted_text = cipher.rail_fence_encrypt(plain_text, key)
    return jsonify({'encrypted_text': encrypted_text})

@app.route('/api/railfence/decrypt', methods=['POST'])
def railfence_decrypt():
    data = request.get_json()
    cipher_text = data.get('cipher_text')
    key = int(data.get('key'))
    cipher = RailFenceCipher()
    decrypted_text = cipher.rail_fence_decrypt(cipher_text, key)
    return jsonify({'decrypted_text': decrypted_text})

# ================= PLAYFAIR API =================
@app.route('/api/playfair/encrypt', methods=['POST'])
def playfair_encrypt():
    data = request.get_json()
    plain_text = data.get('plain_text')
    key = data.get('key')
    cipher = PlayFairCipher()
    matrix = cipher.create_playfair_matrix(key)
    encrypted_text = cipher.playfair_encrypt(plain_text, matrix)
    return jsonify({'encrypted_text': encrypted_text})

@app.route('/api/playfair/decrypt', methods=['POST'])
def playfair_decrypt():
    data = request.get_json()
    cipher_text = data.get('cipher_text')
    key = data.get('key')
    cipher = PlayFairCipher()
    matrix = cipher.create_playfair_matrix(key)
    decrypted_text = cipher.playfair_decrypt(cipher_text, matrix)
    return jsonify({'decrypted_text': decrypted_text})

@app.route('/api/playfair/creatematrix', methods=['POST'])
def playfair_matrix():
    data = request.get_json()
    key = data.get('key')
    cipher = PlayFairCipher()
    matrix = cipher.create_playfair_matrix(key)
    return jsonify({'matrix': matrix})

# ================= TRANSPOSITION API =================
@app.route('/api/transposition/encrypt', methods=['POST'])
def transposition_encrypt():
    data = request.get_json()
    plain_text = data.get('plain_text')
    key = int(data.get('key'))
    cipher = TranspositionCipher()
    encrypted_text = cipher.encrypt(plain_text, key)
    return jsonify({'encrypted_text': encrypted_text})

@app.route('/api/transposition/decrypt', methods=['POST'])
def transposition_decrypt():
    data = request.get_json()
    cipher_text = data.get('cipher_text')
    key = int(data.get('key'))
    cipher = TranspositionCipher()
    decrypted_text = cipher.decrypt(cipher_text, key)
    return jsonify({'decrypted_text': decrypted_text})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)