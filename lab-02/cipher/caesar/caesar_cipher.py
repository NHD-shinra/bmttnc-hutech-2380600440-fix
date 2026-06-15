class CaesarCipher:
    def __init__(self):
        pass

    def encrypt_text(self, text: str, key: int) -> str:
        if not isinstance(key, int) or not (1 <= key <= 25):
            raise ValueError("Key must be an integer between 1 and 25.")
        
        encrypted_text = []
        for letter in text:
            if letter.isupper():
                letter_index = ord(letter) - ord('A')
                output_index = (letter_index + key) % 26
                output_letter = chr(output_index + ord('A'))
                encrypted_text.append(output_letter)
            elif letter.islower():
                letter_index = ord(letter) - ord('a')
                output_index = (letter_index + key) % 26
                output_letter = chr(output_index + ord('a'))
                encrypted_text.append(output_letter)
            else:
                encrypted_text.append(letter)
        return "".join(encrypted_text)

    def decrypt_text(self, text: str, key: int) -> str:
        if not isinstance(key, int) or not (1 <= key <= 25):
            raise ValueError("Key must be an integer between 1 and 25.")
        
        decrypted_text = []
        for letter in text:
            if letter.isupper():
                letter_index = ord(letter) - ord('A')
                output_index = (letter_index - key) % 26
                output_letter = chr(output_index + ord('A'))
                decrypted_text.append(output_letter)
            elif letter.islower():
                letter_index = ord(letter) - ord('a')
                output_index = (letter_index - key) % 26
                output_letter = chr(output_index + ord('a'))
                decrypted_text.append(output_letter)
            else:
                decrypted_text.append(letter)
        return "".join(decrypted_text)