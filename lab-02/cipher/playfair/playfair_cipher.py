class PlayFairCipher:
    def __init__(self):
        pass

    def create_playfair_matrix(self, key):
        if not isinstance(key, str):
            raise ValueError("Key must be a string.")
            
        key = key.replace("J", "I").upper()
        clean_key = []
        for c in key:
            if c.isalpha() and c not in clean_key:
                clean_key.append(c)

        alphabet = "ABCDEFGHIKLMNOPQRSTUVWXYZ"
        matrix = list(clean_key)

        for letter in alphabet:
            if letter not in matrix:
                matrix.append(letter)
                if len(matrix) == 25:
                    break

        playfair_matrix = [matrix[i:i+5] for i in range(0, len(matrix), 5)]
        return playfair_matrix

    def find_letter_coords(self, matrix, letter):
        for row in range(len(matrix)):
            for col in range(len(matrix[row])):
                if matrix[row][col] == letter:
                    return row, col
        raise ValueError(f"Letter {letter} not found in Playfair matrix.")

    def get_playfair_pairs(self, text):
        cleaned = []
        for char in text.upper():
            if char == 'J':
                cleaned.append('I')
            elif char.isalpha():
                cleaned.append(char)
        
        pairs = []
        i = 0
        while i < len(cleaned):
            c1 = cleaned[i]
            if i + 1 < len(cleaned):
                c2 = cleaned[i+1]
                if c1 == c2:
                    pad = 'Q' if c1 == 'X' else 'X'
                    pairs.append(c1 + pad)
                    i += 1
                else:
                    pairs.append(c1 + c2)
                    i += 2
            else:
                pad = 'Q' if c1 == 'X' else 'X'
                pairs.append(c1 + pad)
                i += 1
        return pairs

    def playfair_encrypt(self, plain_text, matrix):
        pairs = self.get_playfair_pairs(plain_text)
        encrypted_text = ""

        for pair in pairs:
            row1, col1 = self.find_letter_coords(matrix, pair[0])
            row2, col2 = self.find_letter_coords(matrix, pair[1])
            if row1 == row2:
                encrypted_text += matrix[row1][(col1 + 1) % 5] + matrix[row2][(col2 + 1) % 5]
            elif col1 == col2:
                encrypted_text += matrix[(row1 + 1) % 5][col1] + matrix[(row2 + 1) % 5][col2]
            else:
                encrypted_text += matrix[row1][col2] + matrix[row2][col1]
        return encrypted_text

    def playfair_decrypt(self, cipher_text, matrix):
        cleaned_cipher = [c for c in cipher_text.upper() if c.isalpha()]
        if len(cleaned_cipher) % 2 != 0:
            raise ValueError("Ciphertext length must be even.")

        decrypted_text = ""
        for i in range(0, len(cleaned_cipher), 2):
            pair = cleaned_cipher[i:i+2]
            row1, col1 = self.find_letter_coords(matrix, pair[0])
            row2, col2 = self.find_letter_coords(matrix, pair[1])

            if row1 == row2:
                decrypted_text += matrix[row1][(col1 - 1) % 5] + matrix[row2][(col2 - 1) % 5]
            elif col1 == col2:
                decrypted_text += matrix[(row1 - 1) % 5][col1] + matrix[(row2 - 1) % 5][col2]
            else:
                decrypted_text += matrix[row1][col2] + matrix[row2][col1]
                
        banro = ""
        i = 0
        while i < len(decrypted_text):
            if i + 2 < len(decrypted_text) and decrypted_text[i] == decrypted_text[i+2] and decrypted_text[i+1] in ('X', 'Q'):
                banro += decrypted_text[i]
                i += 2
            else:
                banro += decrypted_text[i]
                i += 1

        if len(banro) > 0 and banro[-1] in ('X', 'Q'):
            banro = banro[:-1]

        return banro
