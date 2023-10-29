from base64 import *
import sys, os
import codecs
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
#from cryptography.hazmat.primitives.kdf.pbkdf2 import CryptographyUnsupportedError
from cryptography.hazmat.primitives.kdf.pbkdf2 import UnsupportedAlgorithm
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
import main


class encoder():
    def __init__(self, mot:str, cle:str) -> None:
        
        self.mot = mot
        self.cle = cle
        self.key = self.aes_key()
        self.clef = self.genkey()


    def spli(self, mot,long):
        """
        cette fonctoin se charge de diviser une chaine de caractère en sessions contenus dans une liste

        Args:
            mot (str): la chaîne de caractère à diviser
            long (int): la longueur de chaque session
        Return:
            r (list): la list contenant les sessions

        """
        c = len(mot) // long
        r = []
        for i in range(c):
            r.append(mot[i*long:(i+1)*long])
        if len(mot) & long != 0:
            r.append(mot[c*long:len(mot)])
        return r
        


    def cesar(self,mot,cle=4):
        """
        encrypte le mot avec un chiffrement de césar avec la clé

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
        chiffrement de vigenère du mot avec la clé

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

    def vari (self,mot):
        """
        chiffrer le mot d'abbord avec base-32 puis en base-64

        Args:
            mot (undefined): mot à encrypté

        """
        r = b32hexencode(mot.encode())
        r = b64encode(r)
        
        return r.decode()

    def pase (self, mot):
        
        """
        chiffrer le mot d'abbord avec de l'base-85 puis en base-16

        Args:
            mot (str): mot à encryté

        """
        r = b85encode(mot.encode())
        r = b16encode(r)

        return r.decode()


    def rotate2 (self,mot):
        """
        just en rot13

        Args:
            mot (str):

        """
        r = codecs.encode(mot,"rot13")
        return r

    def nine (self,mot) :
        """
        juste base 32

        Args:
            mot (str): mot à encrypté
        """
        
        r = b32hexencode(mot.encode())
        return r.decode()


    def zero(self,mot):
        """
        juste la réutiisation de la fonction vari 

        Args:
            mot (str): mot à encrypter

        """
        r = self.vari(mot)

        return r
    #--------------generer la cle des chriffrements de bases----------

    def genkey(self):
            """
            Génération de la clé utiliser pour encrypter le mot

            Args:
                mdp (str): la clé de chiffrement entrer par l'utiisateur

            """
            od =""
            for i in self.cle:
                od += str(ord(i))
            return od[8:]

    #--------------generer la cle AES----------

    def aes_key(self, salt = b'\xc1g\x98Vbf\xd1\xcdRd\xfe\x8d\xf1\xf4/\x8e'):
        """
        Génération de la clé utiliser pour AES

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
        return self.aes( mot.encode())

if __name__== "__main__":
    enc = encoder("azer", "reza")
    print(enc.crypt())