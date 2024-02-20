import codecs
# import sys,os
from base64 import *
# from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
# from cryptography.hazmat.primitives.ciphers.aead import ChaCha20Poly1305
# from cryptography.hazmat.primitives.kdf.pbkdf2 import UnsupportedAlgorithm
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes


# from cryptography.hazmat.primitives.kdf.pbkdf2 import CryptographyUnsupportedError

class Decoder:
    """ Cette classe crée des objets decoder qui s'occupent de décoder la chaine de caractères
    à l'aide des modues suivants:

    cesar:    un chiffrement de césar
    vignere:  un chiffrement de vigénère
        split: s'occupe sessionner la chaine selon la longueur de la clé vigénère
    base:     encdage par ascii85 et base64
    sub:      chiffrement par substitution
    rotate:   chiffrement par rot13 et par base32
    vari:     chiffrement par CAST5
    pase:     chiffrement par Camellia
    rotate2:  chiffrement par TripleDES
    nine:     chiffrement par BlowFish
    zero:     chiffrement par Chacha20
    crypt:    s'occupe de crypter la chaine en fonction de la clé d'ordre

    la clé d'ordre est l'une des clés générées à partie de la clé entrée par l'utilisateur elle est contituée
    des chiffres représentant chacun un des modules citées précédemment. Elle détermine l'ordre dans lequel
    les modules doivent s'exercuter pour décrypter la chaine
    """

    def __init__(self, mot: str, cle: str) -> None:
        """
        le constructeur de notre classe

        Args:
            mot (str): la chaine à chiffrer
            cle (str): la clé de chiffrement

        """
        self.mot = mot
        self.cle = cle
        self.key = self.aes_key()
        self.clef = self.genkey()

    def spli(self, mot, long) -> list:
        """
        cette fonctoin se charge de diviser une chaine de caractère en sessions
        contenus dans une liste pour le chiffrement de vigénère

        Args:
            mot (str): la chaîne de caractère à diviser
            long (int): la longueur de chaque session
        Return:
            r (list): la list contenant les sessions

        """
        c = len(mot) // long
        r = []
        for i in range(c):
            r.append(mot[i * long:(i + 1) * long])
        if len(mot) % long != 0:
            r.append(mot[c * long:len(mot)])
        return r

    def unpad_string(self, mot):
        """
        fonction d'unpadding

        Args:
            mot (bytes): l'expression a padder

        """
        padding_size = mot[-1]
        return mot[:-padding_size]

    def cesar(self, mot, cle=4) -> str:
        """
        decrypte le mot avec un chiffrement de césar avec la clé

        Args:
            mot (str): le mot à decrypté
            cle (int): la cé
        Return:
            r (str): le mot decrypté 

        """
        r = ''
        for i in mot:
            r += chr(ord(i) - cle)
        return r

    def vignere(self, mot, cle=(2, 3, 3, 1)) -> str:
        """
        déchiffrement de vigenère du mot avec la clé

        Args:
            mot (str): le mot à decrypté
            cle (list): la clé de chiffrement de vigénère
        Return:
            r (str): le mot decrypté
        """
        long = len(cle)
        r = ""
        # count = 0
        l = self.spli(mot=mot, long=long)
        for ex in l:

            for i in range(len(ex)):
                r += chr(ord(ex[i]) - cle[i])
        return r

    def base(self, mot) -> str:
        """
        dechiffrer le mot d'abbord avec  base-64 puis en ascii-85 

        Args:
            mot (str):  le mot à decrypté
        Return:
            r (str): le mot decrypté

        """
        temp = b64decode(mot.encode())
        bas = a85decode(temp)

        return bas.decode()

    def sub(self, mot) -> str:
        """
        dechiffrement du mot par substitution 

        Args:
            mot (str): mot à decrypté 

        """
        r = ""
        sublist = {
            "a": "й", "b": "ц", "c": "у", "d": "к",
            "e": "е", "f": "н", "g": "г", "h": "ш",
            "i": "щ", "j": "з", "k": "х", "l": "ф",
            "m": "ы", "n": "в", "o": "а", "p": "п",
            "q": "р", "r": "о", "s": "л", "t": "д",
            "u": "ж", "v": "э", "w": "я", "x": "ч",
            "y": "с", "z": "м", "A": "Ю", "B": "Б",
            "C": "Ь", "D": "Т", "E": "И", "F": "М",
            "G": "С", "H": "Ч", "I": "Я", "J": "Э",
            "K": "Ж", "L": "Д", "M": "Л", "N": "О",
            "O": "Р", "P": "П", "Q": "А", "R": "В",
            "S": "Ы", "T": "Ф", "U": "Х", "V": "З",
            "W": "Щ", "X": "Ш", "Y": "Г", "Z": "Н"
        }
        for i in sublist.keys():
            mot = mot.replace(sublist[i], i)

        return mot

    def rotate(self, mot) -> str:
        """
        déchiffrer le mot d'abbord avec de rot13 puis en base-32

        Args:
            mot (str): mot a decrypté

        """
        mot = codecs.decode(mot, "rot13")
        r = b32decode(mot.encode())

        return r.decode()

    def vari(self, ciphertext):
        """
        déchiffrement par CAST5

        Args:
            ciphertext (str): chaine à encryptée

        Return: la chaine encrypter 

        """
        k = self.des_key()
        backend = default_backend()
        ciphertext = b64decode(ciphertext.encode())
        iv = ciphertext[:8]
        ciphertext = ciphertext[8:]
        cipher = Cipher(algorithms.CAST5(k), modes.CBC(iv), backend=backend)
        decryptor = cipher.decryptor()
        padded_plaintext = decryptor.update(ciphertext) + decryptor.finalize()
        plaintext = self.unpad_string(padded_plaintext)
        return plaintext.decode()

    def pase(self, ciphertext):
        """
        déchiffrement par Camellia

        Args:
            ciphertext (str): chaine à encryptée

        Return: la chaine encrypter 

        """
        k = self.des_key()
        backend = default_backend()
        ciphertext = b64decode(ciphertext.encode())
        iv = ciphertext[:16]
        ciphertext = ciphertext[16:]
        cipher = Cipher(algorithms.Camellia(k), modes.CBC(iv), backend=backend)
        decryptor = cipher.decryptor()
        padded_plaintext = decryptor.update(ciphertext) + decryptor.finalize()
        plaintext = self.unpad_string(padded_plaintext)
        return plaintext.decode()

    def rotate2(self, ciphertext) -> str:
        """
        déchiffrement par TripleDES

        Args:
            ciphertext (str): chaine à encrypter

        Return: la chaine encrypter 

        """
        k = self.des_key()
        backend = default_backend()
        ciphertext = b64decode(ciphertext.encode())
        iv = ciphertext[:8]
        ciphertext = ciphertext[8:]
        cipher = Cipher(algorithms.TripleDES(k), modes.CBC(iv), backend=backend)
        decryptor = cipher.decryptor()
        padded_plaintext = decryptor.update(ciphertext) + decryptor.finalize()
        plaintext = self.unpad_string(padded_plaintext)
        return plaintext.decode()

    def nine(self, ciphertext) -> str:
        """
        déchiffrement par Blowfish

        Args:
            ciphertext (str): chaine à encrypter

        Return: la chaine encrypter 
        """
        backend = default_backend()
        ciphertext = b64decode(ciphertext.encode())
        iv = ciphertext[:8]
        ciphertext = ciphertext[8:]
        cipher = Cipher(algorithms.Blowfish(self.key), modes.CBC(iv), backend=backend)
        decryptor = cipher.decryptor()
        padded_plaintext = decryptor.update(ciphertext) + decryptor.finalize()
        plaintext = self.unpad_string(padded_plaintext)
        return plaintext.decode()

    def zero(self, mot):
        """
        déchiffrement par Chacha20
        Args:
            mot (str): chaine à encrypter

        Return: la chaine encryptée
        """
        mot = b64decode(mot.encode())
        nonce = mot[:16]
        mot = mot[16:]
        backend = default_backend()
        # Création de l'objet Cipher avec l'algorithme ChaCha20
        cipher = Cipher(algorithms.ChaCha20(self.key, nonce), mode=None, backend=backend)

        # Création de l'objet ChaCha20Poly1305 pour l'authentification
        decryptor = cipher.decryptor()
        # Chiffrement du texte en clair
        ciphertext = decryptor.update(mot) + decryptor.finalize()

        return ciphertext.decode()

    # --------------generer la cle des chriffrements de bases----------
    def genkey(self) -> str:
        """
            Génération de la clé d'ordre

            Args:

            """
        od = ""
        for i in self.cle:
            od += str(ord(i))
        return od[:15]

    # --------------generer la cle AES----------
    def aes_key(self, salt=b'\xc1g\x98Vbf\xd1\xcdRd\xfe\x8d\xf1\xf4/\x8e') -> bytes:
        """
        Génération de la clé utiliser pour AES

        Args:

            salt= (byte): la sel de généraisation

        """
        password = self.cle.encode()
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000
        )
        key = kdf.derive(password)
        return key

    def des_key(self, salt=b'\xc1g\x98Vbf\xd1\xcdRd\xfe\x8d\xf1\xf4/\x8e'):
        """
        Génération de la clé utiliser pour TripleDES

        Args:
            salt= (byte): la sel de généraisation

        """
        password = self.cle.encode()
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=16,
            salt=salt,
            iterations=100000
        )
        key = kdf.derive(password)
        return key

    # --------------chriffrement  AES----------
    def aes(self, mot) -> str:
        """
        la fonction de dechiffrement par AES

        Args:
            mot (str): mot à decrypter

        """
        ciphertext = b64decode(mot.encode())
        iv = ciphertext[:16]
        ciphertext = ciphertext[16:]
        cipher = Cipher(algorithms.AES(self.key), modes.CBC(iv))
        decryptor = cipher.decryptor()
        unpadder = padding.PKCS7(128).unpadder()
        decrypted_data = decryptor.update(ciphertext) + decryptor.finalize()
        plaintext = unpadder.update(decrypted_data) + unpadder.finalize()
        return plaintext.decode()

    def crypt(self) -> str:
        """
        s'occupe de bien gérer la génération des clés de chiffrement et d'appeler les fonctions de dechiffrement
        Args:
        """
        try:
            mot = self.mot
            mot = self.aes(mot)

            dic = {"1": self.cesar, "2": self.vignere, "3": self.base, "4": self.sub, "5": self.rotate,
                   "6": self.vari, "7": self.pase, "8": self.rotate2, "9": self.nine, "0": self.zero}
            for i in self.clef[::-1]:
                mot = dic[i](mot)
                # print(i, ":", mot)
            return mot
        except ValueError:
            print('\033[31m' + "Votre mot de passe est incorrect" + '\033[0m')
            exit()


if __name__ == "__main__":
    dec = Decoder("", "hnbgdmwqazs")
    print(Decoder.pase(dec, "Lutc6LOzaeZV6R91VMnskcTM/BGpk1ZcaDVTPbtgtJo="))
