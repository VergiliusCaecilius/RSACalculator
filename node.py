import hashlib
import my_math_fx

"""Fixed the edge case of 5, 7, and 13."""
class RSAKeyGenerator:
    def __init__(self, p: int, q: int, e: int):
        if my_math_fx.check_prime(p) and my_math_fx.check_prime(q):
            self.p = p
            self.q = q
        else:
            raise ValueError("Both p and q must be prime numbers.")

        # Calculate n and Euler's totient
        self.n = self.p * self.q
        self.euler_product = (self.p - 1) * (self.q - 1)

        # Find a valid public exponent e
        if my_math_fx.are_coprime(e, self.euler_product):
            self.e = e
        else:
            raise ValueError(f"e must be coprime to {self.euler_product}")

        self.d = self.getD()

    def __str__(self):
        return f"""RSA Key Information:
        p = {self.p}
        q = {self.q}
        n = {self.n}
        e = {self.e}
        d = {self.d}
        """

    def __repr__(self):
        return f"RSAKeyGenerator(p={self.p}, q={self.q}, e={self.e}, d={self.d})"

    def getN(self):
        """Return public modulus n."""
        return self.n

    def getE(self):
        """Return public exponent e."""
        return self.e

    def getD(self):
        """Calculate the modular inverse of e mod φ(n)."""
        d = my_math_fx.bezout_coefficients(self.e, self.euler_product)[0]
        # Ensure d is positive
        return d % self.euler_product

    def encrypt(self, message: str, other_node) -> list:
        """Encrypt a message (string) using RSA."""
        encrypted = [pow(ord(char), other_node.e, other_node.n) for char in message]
        return encrypted  # Returns list of encrypted integers

    def decrypt(self, encrypted_message: list) -> str:
        """Decrypt an encrypted message using RSA."""
        decrypted = "".join([chr(pow(chunk, self.d, self.n)) for chunk in encrypted_message])
        return decrypted

    def sign(self, message: str) -> int:
        """Sign a message using the private key."""
        message_hash = int(hashlib.sha256(message.encode()).hexdigest(), 16) % self.n  # Hash then mod n turns string into an int
        return pow(message_hash, self.d, self.n)

    def verify(self, other_node, message: str, signature: int) -> bool:
        """Verify a signed message from another node."""
        decrypted_signature = pow(signature, other_node.e, other_node.n)
        expected_hash = int(hashlib.sha256(message.encode()).hexdigest(), 16) % other_node.n  # Hash then mod n
        return decrypted_signature == expected_hash

    def letter_to_number(self, letter: str) -> str:
        """Convert a letter to a two-digit number (A=01, B=02, ..., Z=26)."""
        num = str(ord(letter.lower()) - ord("a") + 1)
        return num.zfill(2)  # Ensures two-digit format

    def message_to_num(self, message: str) -> str:
        """Convert an entire message to a numeric string representation."""
        return "".join(self.letter_to_number(letter) for letter in message)
    


