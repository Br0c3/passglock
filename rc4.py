
import random
import string
import hashlib
from cryptography.cryptorand import RandomBitGenerator
from cryptography.crypto import BlockCipher
from cryptography.hazmat.backends import default_backend

def encrypt_rc4(plaintext, key):
    # Génération d'un générateur de bits aléatoires
    rand_gen = RandomBitGenerator(key)

    # Initialisation de la fonction de chiffrement RC4
    cipher = BlockCipher(rand_gen.bytes())

    # Chiffrement de la chaîne de caractères
    ciphertext = cipher.encrypt(hashlib.sha256(plaintext.encode('utf-8')).digest())

    # Retour de la chaîne chiffrée
    return ciphertext

def decrypt_rc4(ciphertext, key):
    # Génération d'un générateur de bits aléatoires
    rand_gen = RandomBitGenerator(key)

    # Initialisation de la fonction de déchiffrement RC4
    cipher = BlockCipher(rand_gen.bytes())

    # Déchiffrement de la chaîne de caractères
    plaintext = cipher.decrypt(ciphertext)

    # Retour de la chaîne déchiffrée
    return plaintext.decode('utf-8')

# Exemple d'utilisation
plaintext = "Hello, world!".encode('utf-8')
key = "1234567890"

ciphertext = encrypt_rc4(plaintext, key)
print("Ciphertext: ", ciphertext)

plaintext = decrypt_rc4(ciphertext, key)
print("Plaintext: ", plaintext)