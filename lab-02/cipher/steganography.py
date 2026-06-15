from PIL import Image
import io

class Steganography:
    @staticmethod
    def encode_image(image_bytes, message):
        """
        image_bytes: bytes of the original image
        message: string to be hidden
        returns: bytes of the modified PNG image
        """
        img = Image.open(io.BytesIO(image_bytes))
        # Ensure image is in RGB mode
        if img.mode != 'RGB':
            img = img.convert('RGB')
            
        width, height = img.size
        
        # Convert message to UTF-8 binary string
        encoded_message = message.encode('utf-8')
        binary_message = ''.join(format(byte, '08b') for byte in encoded_message)
        binary_message += '1111111111111110'  # 16-bit marker representing 0xFFFE (255, 254)
        
        total_bits = len(binary_message)
        max_bits = width * height * 3
        if total_bits > max_bits:
            raise ValueError(f"Thông điệp quá dài so với ảnh đã chọn. Kích thước tối đa: {max_bits // 8} bytes, kích thước thông điệp: {len(encoded_message)} bytes.")
            
        pixels = img.load()
        data_index = 0
        
        for row in range(height):
            for col in range(width):
                if data_index >= total_bits:
                    break
                r, g, b = pixels[col, row]
                
                # Modify Red LSB
                if data_index < total_bits:
                    r = (r & ~1) | int(binary_message[data_index])
                    data_index += 1
                # Modify Green LSB
                if data_index < total_bits:
                    g = (g & ~1) | int(binary_message[data_index])
                    data_index += 1
                # Modify Blue LSB
                if data_index < total_bits:
                    b = (b & ~1) | int(binary_message[data_index])
                    data_index += 1
                    
                pixels[col, row] = (r, g, b)
            if data_index >= total_bits:
                break
                
        # Save as PNG to avoid compression issues and keep LSB values exact
        out_buf = io.BytesIO()
        img.save(out_buf, format='PNG')
        return out_buf.getvalue()

    @staticmethod
    def decode_image(image_bytes):
        """
        image_bytes: bytes of the encoded image
        returns: string (decoded message)
        """
        img = Image.open(io.BytesIO(image_bytes))
        if img.mode != 'RGB':
            img = img.convert('RGB')
            
        width, height = img.size
        pixels = img.load()
        
        binary_message = []
        for row in range(height):
            for col in range(width):
                r, g, b = pixels[col, row]
                binary_message.append(str(r & 1))
                binary_message.append(str(g & 1))
                binary_message.append(str(b & 1))
                
        binary_str = "".join(binary_message)
        
        # Convert bits to bytes
        extracted_bytes = bytearray()
        for i in range(0, len(binary_str), 8):
            byte_bits = binary_str[i:i+8]
            if len(byte_bits) < 8:
                break
            val = int(byte_bits, 2)
            extracted_bytes.append(val)
            
            # Check for terminator: 0xFFFE which is [255, 254]
            if len(extracted_bytes) >= 2 and extracted_bytes[-2] == 255 and extracted_bytes[-1] == 254:
                # Remove terminator
                extracted_bytes = extracted_bytes[:-2]
                break
                
        try:
            return extracted_bytes.decode('utf-8')
        except Exception:
            raise ValueError("Không thể giải mã thông điệp từ hình ảnh này. Ảnh có thể không chứa tin giấu hoặc đã bị hỏng.")
