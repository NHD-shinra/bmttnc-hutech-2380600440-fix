from flask import Flask, render_template, request, jsonify, send_file
from cipher.caesar import CaesarCipher
from cipher.vigenere import VigenereCipher
from cipher.railfence import RailFenceCipher
from cipher.playfair import PlayFairCipher
from cipher.steganography import Steganography
import io

app = Flask(__name__)

@app.errorhandler(ValueError)
def handle_value_error(e):
    if request.is_json or request.headers.get('X-Requested-With') == 'XMLHttpRequest' or request.path.startswith('/stego'):
        return jsonify({'error': str(e)}), 400
    return f"<h3>Lỗi Yêu cầu / Request Error</h3><p style='color: red;'>{e}</p><br/><a href='javascript:history.back()'>Quay lại (Go Back)</a>", 400

@app.errorhandler(KeyError)
def handle_key_error(e):
    if request.is_json or request.headers.get('X-Requested-With') == 'XMLHttpRequest' or request.path.startswith('/stego'):
        return jsonify({'error': f"Thiếu tham số bắt buộc: {str(e)}"}), 400
    return f"<h3>Lỗi Yêu cầu / Request Error</h3><p style='color: red;'>Thiếu tham số bắt buộc: {str(e)}</p><br/><a href='javascript:history.back()'>Quay lại (Go Back)</a>", 400

# router routes for home page
@app.route("/")
def home():
    return render_template('index.html')

# ==================== CAESAR CIPHER ====================
@app.route("/caesar")
def caesar():
    return render_template('caesar.html')

@app.route("/encrypt", methods=['POST'])
def caesar_encrypt():
    if request.is_json:
        data = request.json
        text = data.get('inputPlainText', '')
        key = int(data.get('inputKeyPlain', 0))
    else:
        text = request.form['inputPlainText']
        key = int(request.form['inputKeyPlain'])
    
    Caesar = CaesarCipher()
    encrypted_text = Caesar.encrypt_text(text, key)
    
    if request.is_json or request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return jsonify({'success': True, 'result': encrypted_text})
    return f"text: {text}<br/>key: {key}<br/>encrypted text: {encrypted_text}"

@app.route("/decrypt", methods=['POST'])
def caesar_decrypt():
    if request.is_json:
        data = request.json
        text = data.get('inputCipherText', '')
        key = int(data.get('inputKeyCipher', 0))
    else:
        text = request.form['inputCipherText']
        key = int(request.form['inputKeyCipher'])
        
    Caesar = CaesarCipher()
    decrypted_text = Caesar.decrypt_text(text, key)
    
    if request.is_json or request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return jsonify({'success': True, 'result': decrypted_text})
    return f"text: {text}<br/>key: {key}<br/>decrypted text: {decrypted_text}"

# ==================== VIGENERE CIPHER ====================
@app.route("/vigenere")
def vigenere():
    return render_template('vigenere.html')

@app.route("/vigenere_encrypt", methods=['POST'])
def vigenere_encrypt():
    if request.is_json:
        data = request.json
        text = data.get('inputPlainText', '')
        key = data.get('inputKeyPlain', '')
    else:
        text = request.form['inputPlainText']
        key = request.form['inputKeyPlain']
        
    cipher = VigenereCipher()
    encrypted_text = cipher.vigenere_encrypt(text, key)
    
    if request.is_json or request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return jsonify({'success': True, 'result': encrypted_text})
    return f"text: {text}<br/>key: {key}<br/>encrypted text: {encrypted_text}"

@app.route("/vigenere_decrypt", methods=['POST'])
def vigenere_decrypt():
    if request.is_json:
        data = request.json
        text = data.get('inputCipherText', '')
        key = data.get('inputKeyCipher', '')
    else:
        text = request.form['inputCipherText']
        key = request.form['inputKeyCipher']
        
    cipher = VigenereCipher()
    decrypted_text = cipher.vigenere_decrypt(text, key)
    
    if request.is_json or request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return jsonify({'success': True, 'result': decrypted_text})
    return f"text: {text}<br/>key: {key}<br/>decrypted text: {decrypted_text}"

# ==================== RAIL FENCE CIPHER ====================
@app.route("/railfence")
def railfence():
    return render_template('railfence.html')

@app.route("/railfence_encrypt", methods=['POST'])
def railfence_encrypt():
    if request.is_json:
        data = request.json
        text = data.get('inputPlainText', '')
        key = int(data.get('inputKeyPlain', 0))
    else:
        text = request.form['inputPlainText']
        key = int(request.form['inputKeyPlain'])
        
    cipher = RailFenceCipher()
    encrypted_text = cipher.rail_fence_encrypt(text, key)
    
    if request.is_json or request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return jsonify({'success': True, 'result': encrypted_text})
    return f"text: {text}<br/>key: {key}<br/>encrypted text: {encrypted_text}"

@app.route("/railfence_decrypt", methods=['POST'])
def railfence_decrypt():
    if request.is_json:
        data = request.json
        text = data.get('inputCipherText', '')
        key = int(data.get('inputKeyCipher', 0))
    else:
        text = request.form['inputCipherText']
        key = int(request.form['inputKeyCipher'])
        
    cipher = RailFenceCipher()
    decrypted_text = cipher.rail_fence_decrypt(text, key)
    
    if request.is_json or request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return jsonify({'success': True, 'result': decrypted_text})
    return f"text: {text}<br/>key: {key}<br/>decrypted text: {decrypted_text}"

# ==================== PLAYFAIR CIPHER ====================
@app.route("/playfair")
def playfair():
    return render_template('playfair.html')

@app.route("/playfair_encrypt", methods=['POST'])
def playfair_encrypt():
    if request.is_json:
        data = request.json
        text = data.get('inputPlainText', '')
        key = data.get('inputKeyPlain', '')
    else:
        text = request.form['inputPlainText']
        key = request.form['inputKeyPlain']
        
    cipher = PlayFairCipher()
    matrix = cipher.create_playfair_matrix(key)
    encrypted_text = cipher.playfair_encrypt(text, matrix)
    
    if request.is_json or request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return jsonify({'success': True, 'result': encrypted_text})
    return f"text: {text}<br/>key: {key}<br/>encrypted text: {encrypted_text}"

@app.route("/playfair_decrypt", methods=['POST'])
def playfair_decrypt():
    if request.is_json:
        data = request.json
        text = data.get('inputCipherText', '')
        key = data.get('inputKeyCipher', '')
    else:
        text = request.form['inputCipherText']
        key = request.form['inputKeyCipher']
        
    cipher = PlayFairCipher()
    matrix = cipher.create_playfair_matrix(key)
    decrypted_text = cipher.playfair_decrypt(text, matrix)
    
    if request.is_json or request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return jsonify({'success': True, 'result': decrypted_text})
    return f"text: {text}<br/>key: {key}<br/>decrypted text: {decrypted_text}"

# ==================== STEGANOGRAPHY ====================
@app.route("/stego/encode", methods=['POST'])
def stego_encode():
    if 'image' not in request.files or 'message' not in request.form:
        return jsonify({'error': 'Thiếu file ảnh hoặc thông điệp cần giấu.'}), 400
        
    image_file = request.files['image']
    message = request.form['message']
    
    if not image_file.filename:
        return jsonify({'error': 'Không có file ảnh nào được chọn.'}), 400
        
    if not message:
        return jsonify({'error': 'Thông điệp cần giấu không được để trống.'}), 400
        
    try:
        image_bytes = image_file.read()
        encoded_bytes = Steganography.encode_image(image_bytes, message)
        return send_file(
            io.BytesIO(encoded_bytes),
            mimetype='image/png',
            as_attachment=True,
            download_name='encoded_image.png'
        )
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route("/stego/decode", methods=['POST'])
def stego_decode():
    if 'image' not in request.files:
        return jsonify({'error': 'Thiếu file ảnh cần giải mã.'}), 400
        
    image_file = request.files['image']
    if not image_file.filename:
        return jsonify({'error': 'Không có file ảnh nào được chọn.'}), 400
        
    try:
        image_bytes = image_file.read()
        message = Steganography.decode_image(image_bytes)
        return jsonify({'success': True, 'message': message})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

# main function
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5050, debug=True)