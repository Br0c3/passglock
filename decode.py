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
    decrypte le mot avec un chiffrement de césar avec la clé

    Args:
        mot (str): le mot à decrypté
        cle=4 (int): la cé
    Return:
        r (str): le mot decrypté 

    """
    r =''
    for i in mot :
        r += chr(ord(i)-cle)
    return r

def vignere (mot, cle=[2,3,3,1]):
    """
    déchiffrement de vigenère du mot avec la clé

    Args:
        mot (str): le mot à decrypté
        cle (list): la clé de chiffrement de vigénère
    Return:
        r (str): le mot decrypté
    """
    long= len(cle)
    r=""
    count=0
    l = spli(mot,long)
    for ex in l:
        
        for i in range(len(ex)):
            r += chr(ord(ex[i])-cle[i])
    return r

def base (mot):
    """
    dechiffrer le mot d'abbord avec  base-64 puis en ascii-85 

    Args:
        mot (str):  le mot à decrypté
    Return:
        r (str): le mot decrypté

    """
    temp= b64decode(mot.encode())
    bas = a85decode(temp)

    return bas.decode()


def sub (mot):
    """
    dechiffrement du mot par substitution 

    Args:
        mot (str): mot à decrypté 

    """
    r =""
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
        mot = mot.replace(sublist[i],i)

    return mot

def rotate (mot):
    """
    déchiffrer le mot d'abbord avec de rot13 puis en base-32

    Args:
        mot (str): mot a decrypté

    """
    mot = codecs.decode(mot,"rot13")
    r = b32decode(mot.encode())

    return r.decode()

def vari (mot):
    """
    dechiffrer le mot d'abbord avec base-64 puis en base-32

    Args:
        mot (undefined): mot à decrypté

    """
    r = b64decode(mot.encode())
    r = b32hexdecode(r)

    return r.decode()

def pase(mot):
    """
    dechiffrer le mot d'abbord avec de l'base-16 puis en base-85

    Args:
        mot (str): mot à decryté

    """
    r = b16decode(mot.encode())
    r = b85decode(r)

    return r.decode()

def rotate2 (mot):
    """
    juste en rot13

    Args:
        mot (str): mot à décoder

    """
    r = codecs.decode(mot,"rot13")

    return r
def nine (mot):
    """
    base 32

    Args:
        mot (str): mot à decrypté
    """
    r = mot

    return b32hexdecode(r.encode().decode()).decode()

def zero (mot:str):
    """
    juste la réutiisation de la fonction vari 

    Args:
        mot (str): mot à decrypter

    """
    r = mot
    return vari(r)

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
def aes(key, ciphertext):
    """
    la fonction de dechiffrement par AES

    Args:
        key (byte): la clé de chiffrement AES
        plaintext (str): mot à decrypter

    """
    ciphertext = b64decode(ciphertext)
    iv = ciphertext[:16]
    ciphertext = ciphertext[16:]
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
    decryptor = cipher.decryptor()
    unpadder = padding.PKCS7(128).unpadder()
    decrypted_data = decryptor.update(ciphertext) + decryptor.finalize()
    plaintext = unpadder.update(decrypted_data) + unpadder.finalize()
    return plaintext.decode()

def crypt(mot,cle="890"):
    """
    s'occupe de bien gérer la génération des clés de chiffrement et d'appeler les fonctions de dechiffrement

    Args:
        mot (str):mot à decrypter
        cle="fdgs" (str): la clé de chiffrement

    """
    try:
        key = aes_key(cle)
        cle = genkey(cle)
        mot = aes(key, mot.encode())
        dic = {"1":cesar,"2":vignere,"3":base,"4":sub,"5":rotate,"6":vari,"7":pase,"8":rotate2,"9":nine,"0":zero}
        for i in cle[::-1]:
            mot = dic[i](mot)
        return mot
    except ValueError:
        print('\033[31m' + "Votre mot de passe est incorrect" + '\033[0m')
        main.prc()
        
        

