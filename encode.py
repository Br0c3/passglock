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

def spli(mot,long):
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
    


def cesar(mot,cle=4):
    """
    encrypte le mot avec un chiffrement de césar avec la clé

    Args:
        mot (str): le mot à encrypté
        cle=4 (int): la cé
    Return:
        r (str): le mot encrypté 

    """
    r =''
    for i in mot :
        r += chr(ord(i)+cle)
    return r

def vignere (mot, cle=[2,3,3,1]):
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
    l = spli(mot,long)
    for ex in l:
        for i in range(len(ex)):
            r += chr(ord(ex[i])+cle[i])
    return r

def base (mot):
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


def sub (mot):
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


def rotate (mot):
    """
    chiffrer le mot d'abbord avec de base-32 puis en rot13

    Args:
        mot (str): mot a encrypté

    """
    mot = b32encode(mot.encode())
    r = codecs.encode(mot.decode(),"rot13")

    return r

def vari (mot):
    """
    chiffrer le mot d'abbord avec base-32 puis en base-64

    Args:
        mot (undefined): mot à encrypté

    """
    r = b32hexencode(mot.encode())
    r = b64encode(r)
    
    return r.decode()

def pase (mot):
    """
    chiffrer le mot d'abbord avec de l'base-85 puis en base-16

    Args:
        mot (str): mot à encryté

    """
    r = b85encode(mot.encode())
    r = b16encode(r)

    return r.decode()


def rotate2 (mot):
    """
    just en rot13

    Args:
        mot (str):

    """
    r = codecs.encode(mot,"rot13")
    return r

def nine (mot) :
    """
    juste base 32

    Args:
        mot (str): mot à encrypté
    """
    
    r = b32hexencode(mot.encode())
    return r.decode()


def zero(mot):
    """
    juste la réutiisation de la fonction vari 

    Args:
        mot (str): mot à encrypter

    """
    r = vari(mot)

    return r
#--------------generer la cle des chriffrements de bases----------

def genkey(mdp):
        """
        Génération de la clé utiliser pour encrypter le mot

        Args:
            mdp (str): la clé de chiffrement entrer par l'utiisateur

        """
        od =""
        for i in mdp:
            od += str(ord(i))
        return od[8:]

#--------------generer la cle AES----------

def aes_key(password, salt = b'\xc1g\x98Vbf\xd1\xcdRd\xfe\x8d\xf1\xf4/\x8e'):
    """
    Génération de la clé utiliser pour AES

    Args:
        password (str): la clé de chiffrement entrer par l'utiisateur
        salt= (byte): la sel de généraisation

    """
    password = password.encode()
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000
    )
    key = kdf.derive(password)
    return key
#--------------chriffrement  AES----------

def aes(key, plaintext):
    """
    la fonction de chiffrement par AES

    Args:
        key (byte): la clé de chiffrement AES
        plaintext (str): mot à encrypter

    """
    iv = os.urandom(16) 
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
    encryptor = cipher.encryptor()
    padder = padding.PKCS7(128).padder()
    padded_plaintext = padder.update(plaintext) + padder.finalize()
    ciphertext = encryptor.update(padded_plaintext) + encryptor.finalize()
    return b64encode(iv + ciphertext).decode()


def crypt(mot,cle="fdgs"):
    """
    s'occupe de bien gérer la génération des clés de chiffrement et d'appeler les fonctions de chiffrement

    Args:
        mot (str):mot à encrypter
        cle="fdgs" (str): la clé de chiffrement

    """
    key = aes_key(cle)
    cle = genkey(cle)

    dic = {"1":cesar,"2":vignere,"3":base,"4":sub,"5":rotate,"6":vari,"7":pase,"8":rotate2,"9":nine,"0":zero}
    for i in cle:
        mot = dic[i](mot)
    return aes(key, mot.encode())
