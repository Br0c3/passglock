import encode
import decode
import file
import string
import random
import re
from getpass import getpass

Fic = re.compile("^[a-zA-Z0-9_\-]+\.json+$")#regex décrivant le format du fichier

#---------fonction de generation de mot de passe---------
def genpwd():
    #precision du nombre de caractere
    print(":"*14,"GENERATION",":"*14)
    size = input("\n\033[33mCombient de caractères voulez vous que votre chaine contienne? :: \033[0m")
    try:
        size =int(size)
    except:
            print("\033[31m" + "votre choix doit seulement comporter des chiffres" + "\033[0m")
            genpwd()
    #les caracteres autorisee
    car = input("""\n\nLes caractères autorisés \n
        a: pour les caractères ASCII\n
        b: pour les nombres \n
        c: pour des ponctuations\n
      \033[33m(ex:acb pour sélectionner toutes les options) :: \033[0m""")

    carl={"a":string.ascii_letters, "b":string.digits, "c":string.punctuation}
    #formatage des caractere autorisee dans cara
    cara =""
    for i in car :
        try:
            cara+=carl[i]
        except:
            print("\033[31m" + "votre choix doit seulement comporter les lettres a b et c" + "\033[0m")
            genpwd()


    password = ""
    
    #boucle de generation
    for i in range(size):
        password += random.choice(cara)

    return password

#-----------fonction d'encodage de mot de passe-----------
def coded ():
    print(":"*14,"ENCODAGE",":"*14)
    chaine = input("\n\033[33mEntrez le mots de passe a coder :: \033[0m")
    cle = getpass("\n\033[33mEntrez votre clé de chiffrement :: \033[0m")
    enc = encode.encoder(chaine.strip(),cle)
    return enc.crypt()


#-----------fonction de decodage de mot de passe----------- 
def uncoded ():
    print(":"*14,"DECODAGE",":"*14)
    chaine = input("\n\033[33mEntrez le mots de passe a decoder :: \033[0m")
    cle = getpass("\n\033[33mEntrez votre clé de chiffrement ::\033[0m ")
    dec = decode.decoder(chaine, cle)
    return dec.crypt()

#-----------fonction d'ouverture d'un nouveau fichier--------
def init():
    print(":"*14,"INITIAISATION D'UN NOUVEAU FICHIER",":"*14)
    fichier = input("\n\033[33mEntrez le nom du nouveau fichier :: \033[0m")
    if not Fic.fullmatch(fichier):
        raise AssertionError
    key = getpass("\n\033[33mEntrez la clé du nouveau fichier :: \033[0m")
    fic = file.file(fichier, key)
    fichier = fic.f_init()
    scd(fic)

#----------fonction d'ouverture d'un ancien fichier-----------
def save():
    print(":"*14,"OUVETURE D'UN FICHIER",":"*14)
    fichier = input("\n\033[33mEntrez le nom du fichier avec l'extantion csv :: \033[0m")
    if not Fic.fullmatch(fichier):
        raise AssertionError
    key = getpass("\n\033[33mEntrez la clé du fichier :: \033[0m")
    try:
        fic = file.file(fichier, key)
        fichier = fic.f_open()
    except FileNotFoundError:
        print('\033[31m' + "Le fichier que vous avez choisi n'existe pas /!\\" + '\033[0m')
    scd(fic)

#----------fonction d'ajout de données----------
def add(fichier : file.file):
        
    ha = [
        "Nom du site",
        "Identifiant (pseudo, e-mail ou numéro)",
        "Mot de passe"
        ]
    data = [fichier.f_compt()]
    for i in ha:
        if i == "Mot de passe":
            da = input(f"\n\033[33mEntrez [{i}] Tapez <g> pour générer un nouveau {i}:: \033[0m")
            if da == "g":
                da =genpwd()
                print(f"Votre mot de passe est :: \033[32m {da} \033[0m")
        else:
            da = input(f"\n\033[33mEntrez [{i}] :: \033[0m")
        data.append(da)
    enc = encode.encoder(data[3], fichier.key)
    data[3] = enc.crypt()
    fichier.f_add(data= data)

#----------fonction d'ajout de données----------
def mod(fichier : file.file):
    
    ha = [
        "Index",
        "Mot de passe"
        ]
    data = []
    for i in ha:
        if i == "Mot de passe":
            da = input(f"\n\033[33mEntrez [{i}] Tapez <g> pour générer un nouveau {i}:: \033[0m")
            if da == "g":
                da =genpwd()
                print(f"Votre mot de passe est :: \033[32m {da} \033[0m")
        else:
            da = input(f"\n\033[33mEntrez [{i}] :: \033[0m")
            if int(da) > int(fichier.f_compt()) or int(da) < 0:
                print('\033[31m' + "Choisissez un index présent dans votre fichier " + '\033[0m')
                mod(fichier)
        data.append(da)
    #data[1] = encode.crypt(data[1],key)
    fichier.f_mod(index= data[0],mdp= data[1])

#----------fonction d'affichage de données----------
def aff(fichier : file.file):
    fichier.f_list()

def upload():
    print("cette fonction n'est pas encore implèmentè")

#---------------le menu principal-----------
def menup ():
    print ("\n")
    print (":"*14,"MENU PRINCIPAL",":"*14)
    print (""" 
        1 : Générer un mot de passe\n
        2 : Encoder un mot de passe\n
        3 : Decoder un mot de passe\n
        4 : Uploader une sauvegarde sur GOOGLE DRIVE\n
        5 : Ouvrir un nouveau fichier de sauvegarde\n
        6 : Ouvrir une sauvegarde existante \n
        7 : Quitter le programme 
        """)
    choix = input("\033[33mQuelle oppération voulez vous éffectuer ? :: \033[0m")
    return choix

#---------------le menu secondaire--------------
def menus(fichier):
    print(":"*14,"MENU SECONDAIRE",":"*14)
    print("""
        1 : Ajouter des données a la sauvegarde\n
        2 : Modifier un mot de passe \n
        3 : Afficher le fichier\n
        4 : Fermer le fichier\n
        5 : Quitter le programme 
        """)
    choix = input("\033[33mQuelle oppération voulez vous éffectuer ? :: \033[0m")
    return choix

#------------gestion du menu secondaire----------
def scd(fichier : file.file):
    while True:
        choix = menus(fichier)
        dict={"1":add,"2":mod,"3":aff,"4":prc,"5":exit}
        if choix in "123":
            dict[choix](fichier)
        else:
            dict[choix]()

#------------gestion du menu principal----------*
def prc():
    while True:
        choix =menup()
        maindict={"1":genpwd,"2":coded,"3":uncoded,"4":upload, "5":init, "6":save ,"7":exit}
        try:
            result=maindict[choix]()
        except KeyError:
            print('\033[31m' + "Option non prise en charge" + '\033[0m')
            continue
        except AssertionError:
            print('\033[31m' + "Entrez le non du fichier avec l'extantion json " + '\033[0m')
            continue
        print (f"Le resultat de votre opération est :: \033[32m {result} \033[0m")

if __name__ =="__main__":
    prc()
