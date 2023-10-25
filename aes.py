import os
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
#from cryptography.hazmat.primitives.kdf.pbkdf2 import CryptographyUnsupportedError
from cryptography.hazmat.primitives.kdf.pbkdf2 import UnsupportedAlgorithm
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

def derive_key(password, salt):
    """
    Description of derive_key

    Args:
        password (undefined):
        salt (undefined):

    """
    
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000
    )
    key = kdf.derive(password)
    return key

def encrypt(key, plaintext):
    """
    Description of encrypt

    Args:
        key (undefined):
        plaintext (undefined):

    """
    """
    Description of encrypt

    Args:
        key (undefined):
        plaintext (undefined):

    """
   
    iv = os.urandom(16) 
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
    encryptor = cipher.encryptor()
    padder = padding.PKCS7(128).padder()
    padded_plaintext = padder.update(plaintext) + padder.finalize()
    ciphertext = encryptor.update(padded_plaintext) + encryptor.finalize()
    return b64encode(iv + ciphertext).decode()

def decrypt(key, ciphertext):
    """
    Description of decrypt

    Args:
        key (undefined):
        ciphertext (undefined):

    """
    
    ciphertext = b64encode(ciphertext)
    iv = ciphertext[:16]
    ciphertext = ciphertext[16:]
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
    decryptor = cipher.decryptor()
    unpadder = padding.PKCS7(128).unpadder()
    decrypted_data = decryptor.update(ciphertext) + decryptor.finalize()
    plaintext = unpadder.update(decrypted_data) + unpadder.finalize()
    return plaintext.decode()

# Exemple d'utilisation
password = "mot de passe fort".encode()
salt = b'\xc1g\x98Vbf\xd1\xcdRd\xfe\x8d\xf1\xf4/\x8e' # Valeur aléatoire pour le sel
plaintext = "Données à chiffrer".encode()

key = derive_key(password, salt)
print("SATTT :", salt)
ciphertext = encrypt(key, plaintext)
key = derive_key(password, salt)
print("KEEYY :", key)
decrypted_plaintext = decrypt(key, ciphertext)

print(f"Ciphertext: {ciphertext}")
print(f"Plaintext déchiffré: {decrypted_plaintext}")