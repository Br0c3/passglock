from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from base64 import *
import os

def pad_string(s):
    block_size = algorithms.Blowfish.block_size // 8
    padding_size = block_size - (len(s) % block_size)
    padding = bytes([padding_size]) * padding_size
    return s + padding

def unpad_string(s):
    padding_size = s[-1]
    return s[:-padding_size]

def encrypt(key, plaintext):
    backend = default_backend()
    iv = os.urandom(8)
    cipher = Cipher(algorithms.Blowfish(key), modes.CBC(iv), backend=backend)
    encryptor = cipher.encryptor()
    padded_plaintext = pad_string(plaintext)
    ciphertext = encryptor.update(padded_plaintext) + encryptor.finalize()
    return b64encode(iv + ciphertext).decode()

def decrypt(key, ciphertext):
    backend = default_backend()
    ciphertext = b64decode(ciphertext.encode())
    print(ciphertext)
    iv = ciphertext[:8]
    ciphertext = ciphertext[8:]
    cipher = Cipher(algorithms.Blowfish(key), modes.CBC(iv), backend=backend)
    decryptor = cipher.decryptor()
    padded_plaintext = decryptor.update(ciphertext) + decryptor.finalize()
    plaintext = unpad_string(padded_plaintext)
    return plaintext

def main():
    key = b'\xf7\xbbFC\xf9\xe0 \x8a\xb2\xe6\xd5\xab\xea\xf1\xac\xeb\xc3I\xce|\xb8\x7fG@\x00t\xcdf\x1b\x83?\xe1'
    plaintext = b"passGlock45"
    t = "jDjouU+Pou96cPbTG5hCsQ=="
    
    encrypted = encrypt(key, plaintext)
    decrypted = decrypt(key, encrypted)
    
    print("Plaintext:", plaintext)
    print("Encrypted:", encrypted)
    print("Decrypted:", decrypted)

if __name__ == "__main__":
    main()