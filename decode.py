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
from cryptography.hazmat.primitives.ciphers.aead import ChaCha20Poly1305
from cryptography.hazmat.backends import default_backend

class decoder():
    
    def __init__(self, mot:str, cle:str) -> None:
        
        self.mot = mot
        self.cle = cle
        self.key = self.aes_key()
        self.clef = self.genkey()




    def spli(self ,mot, long) -> list:
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
        if len(mot) % long != 0:
            r.append(mot[c*long:len(mot)])
        return r

    def pad_string(self, mot):
        block_size = algorithms.Blowfish.block_size // 8
        padding_size = block_size - (len(mot) % block_size)
        padding = bytes([padding_size]) * padding_size
        return mot + padding
    
    def pad_desstring(self, mot):
        block_size = algorithms.TripleDES.block_size // 8
        padding_size = block_size - (len(mot) % block_size)
        padding = bytes([padding_size]) * padding_size
        return mot + padding

    def unpad_string(self, mot):
        padding_size = mot[-1]
        return mot[:-padding_size]

    def cesar(self, mot, cle=4) -> str:
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

    def vignere (self, mot, cle=[2,3,3,1]) -> str:
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
        l = self.spli(mot=mot, long=long)
        for ex in l:
            
            for i in range(len(ex)):
                r += chr(ord(ex[i])-cle[i])
        return r

    def base (self, mot)-> str:
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


    def sub (self,mot) -> str:
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

    def rotate (self, mot) -> str:
        """
        déchiffrer le mot d'abbord avec de rot13 puis en base-32

        Args:
            mot (str): mot a decrypté

        """
        mot = codecs.decode(mot,"rot13")
        r = b32decode(mot.encode())

        return r.decode()

    def vari (self, mot) -> str:
        """
        dechiffrer le mot d'abbord avec base-64 puis en base-32

        Args:
            mot (undefined): mot à decrypté

        """
        r = b64decode(mot.encode())
        r = b32hexdecode(r)

        return r.decode()

    def pase(self, mot) -> str:
        """
        dechiffrer le mot d'abbord avec de l'base-16 puis en base-85

        Args:
            mot (str): mot à decryté

        """
        r = b16decode(mot.encode())
        r = b85decode(r)

        return r.decode()
    
    def rotate2 (self, ciphertext) -> str:
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
    
    def nine (self, ciphertext) -> str:

        backend = default_backend()
        ciphertext = b64decode(ciphertext.encode())
        iv = ciphertext[:8]
        ciphertext = ciphertext[8:]
        cipher = Cipher(algorithms.Blowfish(self.key), modes.CBC(iv), backend=backend)
        decryptor = cipher.decryptor()
        padded_plaintext = decryptor.update(ciphertext) + decryptor.finalize()
        plaintext = self.unpad_string(padded_plaintext)
        return plaintext.decode()

    def zero(self,mot):
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

    #--------------generer la cle des chriffrements de bases----------
    def genkey(self) -> str:
            """
            Génération de la clé utiliser pour encrypter le mot

            Args:
                mdp (str): la clé de chiffrement entrer par l'utiisateur

            """
            od =""
            for i in self.cle:
                od += str(ord(i))
            return od[:15]

    #--------------generer la cle AES----------
    def aes_key(self, salt = b'\xc1g\x98Vbf\xd1\xcdRd\xfe\x8d\xf1\xf4/\x8e') -> bytes:
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
    

    def des_key(self, salt = b'\xc1g\x98Vbf\xd1\xcdRd\xfe\x8d\xf1\xf4/\x8e'):
        """
        Génération de la clé utiliser pour AES

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
    def aes(self, mot) -> str:
        """
        la fonction de dechiffrement par AES

        Args:
            key (byte): la clé de chiffrement AES
            plaintext (str): mot à decrypter

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
            mot (str):mot à decrypter
            cle="fdgs" (str): la clé de chiffrement
        """
        try:
            mot = self.mot
            mot = self.aes(mot)
                
            dic = {"1":self.cesar, "2":self.vignere, "3":self.base,    "4":self.sub,  "5":self.rotate,
                "6":self.vari,  "7":self.pase,    "8":self.rotate2, "9":self.nine, "0":self.zero}
            for i in self.clef[::-1]:
                mot = dic[i](mot)
                #print(i, ":", mot)
            return mot
        except ValueError:
            print('\033[31m' + "Votre mot de passe est incorrect" + '\033[0m')
            exit()
            
        
if __name__== "__main__":
    dec = decoder("ZfmemB+8oWjAMgGT3m4390XEB/9nfUSrUn4nLAt9KPe4r2O4fJtdu9wVLQbzR4s8b/Qbjz6Jiqyngnnmpw4aFYGbV6y6IMZeHJh7ZvtOvR37Ffh6KtUEvLs55aziUOaNO0bLH5HJUMsNggGQHWPS1MK2oi42ZM4i8q7U+xFkCtkCSSS16i0MWJt1QC5xV289m6VKpBOO9U9kXvn4VwN9L5BuARCNZiTLN5LUY+n86R8rEBLvtY4xcXpEXwmy1CjkTOAXi0ank/0rCpSozBK0uzTI4Nr+Cebp5wQP/aIrea43V2VLCOdmmk+aJB0naRWQFyyp5M8GSWLYYxTjjCm1wzVkJxmjGQ5SJL3gPULv48BOC9qA6ax7MIRiPjezUmB34Mo2cna4gHiYkyPjFqqGhJ/Iv6RfHZkMsxouSgYf7TO5cGVQ6n28RnNhUgEiEp/0j4FpTG2SuJXp8Wp5XIWkXCC0V/vK2vk31CorKCRWr+PjnqO/1AWSH4EI79I8RhPUOusAyfFTRo94R3vRHZsnRR69am9IRuAPO5r1dPX2tEpTWk2KjXaOEDCxMj68/rIgHmHA+RUienIwypkY0UyhPTZahx+5szEArnleKx9g9DQ+6y4QQbetNkUunQckzNbCsayv1SdPojm1c0DXpVIxb5xk7qoe6oGE+xB1VQeMV9r6SrahsUV/uEukW8Svr9N3qgvjcbbu1yQ42y5hd6/cAiO96tONv+g9B7QNyF4MlKSeMLCWgIiFOAebpzcSp5RiDwPkvkUdZ9sPF5aXnx2LWvUp+F72SpB/GP/ZLHsgxJM1uuuw0xLbFIsHjfXbxyjnfRUgIoLyy0GFIGRyx6dCTbF9s2/DtZtNuc+xE/cyY+vM0NqHJLDj2rxTIFwrXG5PyUZLSvZ8rVCTdNitwDPyUlx+PVovv9yk13dci8pWZMG9SvHuEP1hw50BqGHyHiKw33R6VQT4RPNeEbtfhA4JZi/5iwQkK0YqVvBdvPljNK/QShuXEoLNO8oPPnvR3cgg", "passkeyyy")
    print(decoder.crypt(dec))