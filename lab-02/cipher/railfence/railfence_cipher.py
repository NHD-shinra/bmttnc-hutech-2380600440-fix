class RailFenceCipher:
    def __init__(self):
        pass

    def validate_key(self, text, num_rails):
        if not isinstance(num_rails, int) or num_rails < 2:
            raise ValueError("Key (number of rails) must be an integer greater than or equal to 2.")
        if len(text) <= num_rails:
            raise ValueError("Key (number of rails) must be strictly less than the text length (which is currently {}).".format(len(text)))

    def rail_fence_encrypt(self, plain_text, num_rails):
        self.validate_key(plain_text, num_rails)
        rails = [[] for _ in range(num_rails)]
        rail_index = 0
        direction = 1  # 1: down, -1: up
        for char in plain_text:
            rails[rail_index].append(char)
            if rail_index == 0:
                direction = 1
            elif rail_index == num_rails - 1:
                direction = -1
            rail_index += direction
        cipher_text = ''.join(''.join(rail) for rail in rails)
        return cipher_text
    
    def rail_fence_decrypt(self, cipher_text, num_rails):
        self.validate_key(cipher_text, num_rails)
        rail_lengths = [0] * num_rails
        rail_index = 0
        direction = 1

        for _ in range(len(cipher_text)):
            rail_lengths[rail_index] += 1
            if rail_index == 0:
                direction = 1
            elif rail_index == num_rails - 1:
                direction = -1
            rail_index += direction

        rails = []
        start = 0
        for length in rail_lengths:
            rails.append(cipher_text[start:start + length])
            start += length

        plain_text = ""
        rail_index = 0
        direction = 1

        for _ in range(len(cipher_text)):
            plain_text += rails[rail_index][0]
            rails[rail_index] = rails[rail_index][1:]
            if rail_index == 0:
                direction = 1
            elif rail_index == num_rails - 1:
                direction = -1
            rail_index += direction

        return plain_text
