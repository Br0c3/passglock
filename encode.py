#!/usr/bin/python3
# -*- coding: utf-8 -*-
import codecs
import sys,os
#import django
from base64 import *
#from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
#from cryptography.hazmat.primitives.ciphers.aead import ChaCha20Poly1305
#from cryptography.hazmat.primitives.kdf.pbkdf2 import UnsupportedAlgorithm
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
#from cryptography.hazmat.primitives.kdf.pbkdf2 import CryptographyUnsupportedError

class Encoder():
    """ Cette classe crée des objets encoder qui s'occupent d'encoder la chaine de caractères 
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

    la clé d'ordre est l'une des clés générées à partie de la clé entrée par l'utilisateur elle est contituée des chiffres 
    représentant chacun un des modules citées précédemment. Elle détermine l'ordre dans lequel les modules doivent s'exercuter 
    pour crypter la chaine
    """
    
    def __init__(self, mot:str, cle:str) -> None:
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


    def spli(self, mot,long):
        """
        cette fonctoin se charge de diviser une chaine de caractère en sessions 
        contenus dans une liste pour le chiffrement de vigénère

        Args:
            mot (str): la chaîne de caractère à sessionner
            long (int): la longueur de chaque session
        Return:
            r (list): la list contenant les sessions

        """
        c = len(mot) // long
        r = []
        for i in range(c):
            r.append(mot[i*long:(i+1)*long])
        if len(mot) % long != 0:
            r.append(mot[c*long:len(mot)])
        return r
        

    def pad_string(self, mot:bytes):
        """
        fonction de padding Blowfish

        Args:
            mot (bytes): l'expression a padder

        """
        block_size = algorithms.Blowfish.block_size // 8
        padding_size = block_size - (len(mot) % block_size)
        padding = bytes([padding_size]) * padding_size
        return mot + padding
    
    def pad_desstring(self, mot):
        """
        fonction de padding TripleDES

        Args:
            mot (bytes): l'expression a padder

        """
        block_size = algorithms.TripleDES.block_size // 8
        padding_size = block_size - (len(mot) % block_size)
        padding = bytes([padding_size]) * padding_size
        return mot + padding
    
    def pad_casstring(self, mot):
        """
        fonction de padding CAST5

        Args:
            mot (bytes): l'expression a padder

        """
        block_size = algorithms.CAST5.block_size // 8
        padding_size = block_size - (len(mot) % block_size)
        padding = bytes([padding_size]) * padding_size
        return mot + padding
    
    def pad_camstring(self, mot):
        """
        fonction de padding Camellia

        Args:
            mot (bytes): l'expression a padder

        """
        block_size = algorithms.Camellia.block_size // 8
        padding_size = block_size - (len(mot) % block_size)
        padding = bytes([padding_size]) * padding_size
        return mot + padding

    def cesar(self,mot,cle=4):
        """
        encrypte le mot avec un chiffrement de césar

        Args:
            mot (str): le mot à encrypté
            cle=4 (int): la clé
        Return:
            r (str): le mot encrypté 

        """
        r =''
        for i in mot :
            r += chr(ord(i)+cle)
        return r

    def vignere (self,mot, cle=[2,3,3,1]):
        """
        chiffrement de vigenère du mot 

        Args:
            mot (str): le mot à encrypté
            cle (list): la clé de chiffrement de vigénère
        Return:
            r (str): le mot encrypté
        """
        long= len(cle)
        r=""
        count=0
        l = self.spli(mot=mot,long=long)
        for ex in l:
            for i in range(len(ex)):
                r += chr(ord(ex[i])+cle[i])
        return r

    def base (self,mot):
        """
        chiffrer le mot d'abbord avec de l'ascii-85 puis en base-64 

        Args:
            mot (str):  le mot à encrypté
        Return:
            r (str): le mot encrypté

        """
        temp= a85encode(mot.encode()) 
        bas = b64encode(temp)

        return bas.decode()


    def sub (self,mot):
        
        """
        chiffrement du mot par substitution 

        Args:
            mot (str):mot à encrypter

        """
        sublist = {
                    "a":"й","b":"ц","c":"у","d":"к",
                    "e":"е","f":"н","g":"г","h":"ш",
                    "i":"щ","j":"з","k":"х","l":"ф",
                    "m":"ы","n":"в","o":"а","p":"п",
                    "q":"р","r":"о","s":"л","t":"д",
                    "u":"ж","v":"э","w":"я","x":"ч",
                    "y":"с","z":"м","A":"Ю","B":"Б",
                    "C":"Ь","D":"Т","E":"И","F":"М",
                    "G":"С","H":"Ч","I":"Я","J":"Э",
                    "K":"Ж","L":"Д","M":"Л","N":"О",
                    "O":"Р","P":"П","Q":"А","R":"В",
                    "S":"Ы","T":"Ф","U":"Х","V":"З",
                    "W":"Щ","X":"Ш","Y":"Г","Z":"Н"
                }
        for i in sublist.keys():
            mot = mot.replace(i,sublist[i])
        return mot


    def rotate (self,mot):
        """
        chiffrer le mot d'abbord avec de base-32 puis en rot13

        Args:
            mot (str): mot a encrypté

        """
        mot = b32encode(mot.encode())
        r = codecs.encode(mot.decode(),"rot13")

        return r

    def vari (self, plaintext:str):
        """
        chiffrement par CAST5

        Args:
            plaintext (str): chaine à encryptée

        Return: la chaine encrypter 

        """
        k = self.des_key()
        backend = default_backend()
        iv = os.urandom(8)
        cipher = Cipher(algorithms.CAST5(k), modes.CBC(iv), backend=backend)
        encryptor = cipher.encryptor()
        padded_plaintext = self.pad_casstring(plaintext.encode())
        ciphertext = encryptor.update(padded_plaintext) + encryptor.finalize()
        return b64encode(iv + ciphertext).decode()

    def pase (self, plaintext):
        """
        chiffrement par Camellia

        Args:
            plaintext (str): chaine à encryptée

        Return: la chaine encrypter 

        """
        k = self.des_key()
        backend = default_backend()
        iv = os.urandom(16)
        cipher = Cipher(algorithms.Camellia(k), modes.CBC(iv), backend=backend)
        encryptor = cipher.encryptor()
        padded_plaintext = self.pad_camstring(plaintext.encode())
        ciphertext = encryptor.update(padded_plaintext) + encryptor.finalize()
        return b64encode(iv + ciphertext).decode()


    def rotate2 (self,plaintext):
        """
        chiffrement par TripleDES

        Args:
            plaintext (str): chaine à encrypter

        Return: la chaine encrypter 

        """
        k = self.des_key()
        backend = default_backend()
        iv = os.urandom(8)
        cipher = Cipher(algorithms.TripleDES(k), modes.CBC(iv), backend=backend)
        encryptor = cipher.encryptor()
        padded_plaintext = self.pad_desstring(plaintext.encode())
        
        ciphertext = encryptor.update(padded_plaintext) + encryptor.finalize()
        return b64encode(iv + ciphertext).decode()

    def nine (self,plaintext) :
        """
        chiffrement par Blowfish

        Args:
            plaintext (str): chaine à encrypter

        Return: la chaine encrypter 
        """
        backend = default_backend()
        iv = os.urandom(8)
        cipher = Cipher(algorithms.Blowfish(self.key), modes.CBC(iv), backend=backend)
        encryptor = cipher.encryptor()
        padded_plaintext = self.pad_string(plaintext.encode())
        ciphertext = encryptor.update(padded_plaintext) + encryptor.finalize()
        return b64encode(iv + ciphertext).decode()


    def zero(self,mot):
        """
        chiffrement par Chacha20
        Args:
            plaintext (str): chaine à encrypter

        Return: la chaine encryptée
        """
        backend = default_backend()
        nonce = os.urandom(16)  # Nonce
        # Création de l'objet Cipher avec l'algorithme ChaCha20
        cipher = Cipher(algorithms.ChaCha20(self.key, nonce), mode=None, backend=backend)

        # Création de l'objet ChaCha20Poly1305 pour l'authentification
        encryptor = cipher.encryptor()
        # Chiffrement du texte en clair
        ciphertext = encryptor.update(mot.encode()) + encryptor.finalize()

        return b64encode(nonce + ciphertext).decode()
    #--------------generer la cle des chriffrements de bases----------

    def genkey(self):
            """
            Génération de la clé d'ordre utilisée pour encrypter le mot

            Args:
                mdp (str): la clé de chiffrement entrer par l'utiisateur

            """
            od =""
            for i in self.cle:
                od += str(ord(i))
            return od[:15]

    #--------------generer la cle AES----------

    def aes_key(self, salt = b'\xc1g\x98Vbf\xd1\xcdRd\xfe\x8d\xf1\xf4/\x8e'):
        """
        Génération de la clé AES

        Args:
            password (str): la clé de chiffrement entrer par l'utiisateur
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
    
    def des_key(self, salt = b'\xc1g\x98Vbf\xd1\xcdRd\xfe\x8d\xf1\xf4/\x8e'):
        """
        Génération de la clé utiliser pour TripleDES

        Args:
            password (str): la clé de chiffrement entrer par l'utiisateur
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
    #--------------chriffrement  AES----------

    def aes(self, plaintext):
        """
        la fonction de chiffrement par AES

        Args:
            key (byte): la clé de chiffrement AES
            plaintext (str): mot à encrypter

        """
        iv = os.urandom(16) 
        cipher = Cipher(algorithms.AES(self.key), modes.CBC(iv))
        encryptor = cipher.encryptor()
        padder = padding.PKCS7(128).padder()
        padded_plaintext = padder.update(plaintext) + padder.finalize()
        ciphertext = encryptor.update(padded_plaintext) + encryptor.finalize()
        return b64encode(iv + ciphertext).decode()


    def crypt(self):
        """
        s'occupe de bien gérer la génération des clés de chiffrement et d'appeler les fonctions de chiffrement

        Args:
            mot (str):mot à encrypter
            cle="fdgs" (str): la clé de chiffrement

        """
        
        mot = self.mot
        dic = {"1":self.cesar,"2":self.vignere,"3":self.base,    "4":self.sub,  "5":self.rotate,
               "6":self.vari, "7":self.pase,   "8":self.rotate2, "9":self.nine, "0":self.zero}
        for i in self.clef:
            mot = dic[i](mot)
            #print(i, ":", mot)
        
        return self.aes( mot.encode())

if __name__== "__main__":
    enc = Encoder("password", "hnbgdmwqazs")
    print(Encoder.pase(enc,"kaz"))