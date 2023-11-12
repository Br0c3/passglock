from cryptography.hazmat.primitives.ciphers import Cipher, algorithms
from cryptography.hazmat.primitives.ciphers.aead import ChaCha20Poly1305
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import os


def encrypt(plaintext, password):
    salt = b'salt'  # Sel
    iterations = 1000  # Nombre d'itérations
    backend = default_backend()

    # Génération de la clé à partir du mot de passe
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=16,
        salt=salt,
        iterations=iterations,
        backend=backend
    )
    key = kdf.derive(password)

    # Génération d'un nonce aléatoire
    nonce = b'\xf4\x82NDu\xa4\xf9$\xdd\x00\x0f\xbf2\xb2\x87P'  # Nonce
    print(nonce[:16])
    # Création de l'objet Cipher avec l'algorithme ChaCha20
    cipher = Cipher(algorithms.ChaCha20(key, nonce), mode=None, backend=backend)

    # Création de l'objet ChaCha20Poly1305 pour l'authentification
    encryptor = cipher.encryptor()

    # Chiffrement du texte en clair
    ciphertext = encryptor.update(plaintext) + encryptor.finalize()

    return ciphertext

def decrypt(plaintext, password):
    salt = b'salt'  # Sel
    iterations = 1000  # Nombre d'itérations
    backend = default_backend()

    # Génération de la clé à partir du mot de passe
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=16,
        salt=salt,
        iterations=iterations,
        backend=backend
    )
    key = kdf.derive(password)

    # Génération d'un nonce aléatoire
    nonce = b'\xf4\x82NDu\xa4\xf9$\xdd\x00\x0f\xbf2\xb2\x87P'  # Nonce

    # Création de l'objet Cipher avec l'algorithme ChaCha20
    cipher = Cipher(algorithms.ChaCha20(key, nonce), mode=None, backend=backend)

    # Création de l'objet ChaCha20Poly1305 pour l'authentification
    encryptor = cipher.decryptor()

    # Chiffrement du texte en clair
    ciphertext = encryptor.update(plaintext)+encryptor.finalize()

    return ciphertext
# Exemple d'utilisation
plaintext = b'Hello, world!'  # Texte en clair à chiffrer
password = b'secret password'  # Mot de passe pour générer la clé

ciphertext = encrypt(plaintext, password)
car = decrypt(ciphertext, password)
print("Texte chiffré :", ciphertext.hex(), car)
