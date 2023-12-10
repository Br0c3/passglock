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
    print(":"*14,"GENERATION",":"*14)
    #precision du nombre de caractere
    size = input("\n\033[33mCombient de caractères voulez vous que votre chaine contienne? :: \033[0m")
    #vérifier l'entrer de l'utilisateur
    try:
        size =int(size)
    except:
            print("\033[31m" + "votre choix doit seulement comporter des chiffres" + "\033[0m")
            # rappeler la fonction si l'erreur est relever
            genpwd()
    #les caracteres autorisee
    car = input("""\n\nLes caractères autorisés \n
        a: pour les caractères ASCII\n
        b: pour les nombres \n
        c: pour des ponctuations\n
      \033[33m(ex:acb pour sélectionner toutes les options) :: \033[0m""")
    # ce dictionnaire aide à faire correspondre les lettres sélectionner avec les types de caractère
    carl={"a":string.ascii_letters, "b":string.digits, "c":string.punctuation}
    #formatage des caractere autorisee dans cara
    cara =""
    for i in car :
        # pour concatener proprement les chaines de caractère dans cara ln vérifie si chaque caractère est une clé du dict carl(a,b,c)
        try:
            cara+=carl[i]
        except:
            print("\033[31m" + "votre choix doit seulement comporter les lettres a b et c" + "\033[0m")
             # rappeler la fonction si l'erreur est relever
            genpwd()
            
    password = ""
    
    #boucle de generation en sélectionnant les caractères au hasard dans le str cara
    for i in range(size):
        password += random.choice(cara)
    #retourner la chaine de caractère générée
    return password

#-----------fonction d'encodage de mot de passe-----------
def coded ():
    print(":"*14,"ENCODAGE",":"*14)
    # prise de la chaine à encoder
    chaine = input("\n\033[33mEntrez la chaine a encoder :: \033[0m")
     # prise de la clé de chiffrement
    cle = getpass("\n\033[33mEntrez votre clé de chiffrement :: \033[0m")
    # construction de l'objet encoder
    enc = encode.Encoder(chaine.strip(),cle)
    # codage
    return enc.crypt()


#-----------fonction de decodage de mot de passe----------- 
def uncoded ():
    print(":"*14,"DECODAGE",":"*14)
     # prise de la chaine à decoder
    chaine = input("\n\033[33mEntrez le mots de passe a decoder :: \033[0m")
     # prise de la clé de chiffrement
    cle = getpass("\n\033[33mEntrez votre clé de chiffrement ::\033[0m ")
    # construction de l'objet decoder
    dec = decode.Decoder(chaine, cle)
    return dec.crypt()

#-----------fonction d'ouverture d'un nouveau fichier--------
def init():
    print(":"*14,"INITIAISATION D'UN NOUVEAU FICHIER",":"*14)
    # le nom du fichier
    fichier = input("\n\033[33mEntrez le nom du nouveau fichier :: \033[0m")
    # vérifier si le nom entré correspond avec le format attendu
    if not Fic.fullmatch(fichier):
        #relever une erreur
        raise AssertionError
    # prise de la clé de chiffrement
    key = getpass("\n\033[33mEntrez la clé du nouveau fichier :: \033[0m")
    fic = file.File(fichier, key)
    # initialliser le fichier
    fichier = fic.f_init()
    # lancer menu secondaire
    scd(fic)

#----------fonction d'ouverture d'un ancien fichier-----------
def save():
    print(":"*14,"OUVETURE D'UN FICHIER",":"*14)
    # le nom du fichier
    fichier = input("\n\033[33mEntrez le nom du fichier avec l'extantion csv :: \033[0m")
    # vérifier si le nom entré correspond avec le format attendu
    if not Fic.fullmatch(fichier):
        #relever une erreur
        raise AssertionError
    # prise de la clé de chiffrement
    key = getpass("\n\033[33mEntrez la clé du fichier :: \033[0m")
    #essayer d'ouvrir le fichier
    try:
        fic = file.File(fichier, key)
        fichier = fic.f_open()
    except FileNotFoundError:#intercepter une erreur si le fichier n'existe pas
        print('\033[31m' + "Le fichier que vous avez choisi n'existe pas /!\\" + '\033[0m')
    # lancer menu secondaire
    scd(fic)

#----------fonction d'ajout de données a un objet File----------
def add(fichier : file.File):
    #liste des données à collecter  
    ha = [
        "Nom du site",
        "Identifiant (pseudo, e-mail ou numéro)",
        "Mot de passe"
        ]
    
    data = [fichier.f_compt()] #numéro d'index de notre dernière sauvegarde au premier indice de la nouvelle liste data
    # parcourir la liste de données
    for i in ha:
        # si la donnée demander est le mot de passe, 
        if i == "Mot de passe":
            #proposer de générer le mot de passe 
            da = input(f"\n\033[33mEntrez [{i}] Tapez <g> pour générer un nouveau {i}:: \033[0m")
            # si proposition selectionner, alors lancer la fonction de génération
            if da == "g":
                da =genpwd()
                print(f"Votre mot de passe est :: \033[32m {da} \033[0m")
        #sinon recupérer la donnée dans la variable da
        else:
            da = input(f"\n\033[33mEntrez [{i}] :: \033[0m")
        # ajouter a chaque e contenue de da dans la liste data
        data.append(da)
    # encoder le mot de pass a l'indice 3 de data
    enc = encode.Encoder(data[3], fichier.key)
    data[3] = enc.crypt()
    # enfin ajouter les données au fichier
    fichier.f_add(data= data)

#----------fonction de modification de données sur un objet File----------
def mod(fichier : file.File):
    #liste des données à collecter 
    ha = [
        "Index",
        "Mot de passe"
        ]
    #une liste vide data
    data = []
    for i in ha: # parcourir la liste de données
        if i == "Mot de passe": # si la donnée demander est le mot de passe, 
            da = input(f"\n\033[33mEntrez [{i}] Tapez <g> pour générer un nouveau {i}:: \033[0m")
            if da == "g": # si proposition selectionner, alors lancer la fonction de génération
                da =genpwd()
                print(f"Votre mot de passe est :: \033[32m {da} \033[0m")
        else: #si la donnée demander est l'index, 
            da = input(f"\n\033[33mEntrez [{i}] :: \033[0m")
            # si numéro d'index de notre dernière sauvegarde est inferieur a l'index entrer ou l'index entrer est négatif
            if int(da) > int(fichier.f_compt()) or int(da) < 0:
                print('\033[31m' + "Choisissez un index présent dans votre fichier " + '\033[0m')
                mod(fichier)
        data.append(da)
    #data[1] = encode.crypt(data[1],key)
    # enfin enregistrer les enrégistrements
    fichier.f_mod(index= data[0],mdp= data[1])

#----------fonction d'affichage de données----------
def aff(fichier : file.File):
    fichier.f_list()


#---------------le menu principal-----------
def menup ():
    print ("\n")
    print (":"*14,"MENU PRINCIPAL",":"*14)
    print (""" 
        1 : Générer un mot de passe\n
        2 : Encoder un mot de passe\n
        3 : Decoder un mot de passe\n
        4 : Ouvrir un nouveau fichier de sauvegarde\n
        5 : Ouvrir une sauvegarde existante \n
        6 : Quitter le programme 
        """)
    # récupérer le choix
    choix = input("\033[33mQuelle oppération voulez vous éffectuer ? :: \033[0m")
    # retourner le choix 
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
    # récupérer le choix
    choix = input("\033[33mQuelle oppération voulez vous éffectuer ? :: \033[0m")
    # retourner le choix
    return choix

#------------gestion du menu secondaire----------
def scd(fichier : file.File):
    while True: # boucle infini
        choix = menus(fichier) # recuperer le choix de l'utilisaeur a partie du menu secondaire 
        # dictionnaire de correspondance entre les choix et les fonctions
        dict={"1":add,"2":mod,"3":aff,"4":prc,"5":exit}
        if choix in "123": # les fonctions ayants besoin de paramettre
            dict[choix](fichier)
        elif choix in "45": # les autres fonctions
            dict[choix]()
        else:
            print('\033[31m' + "Option non prise en charge" + '\033[0m')

#------------gestion du menu principal----------*
def prc():
    while True: # boucle infini
        choix =menup() # recuperer le choix de l'utilisaeur a partie du menu principal
        # dictionnaire de correspondance entre les choix et les fonctions
        maindict={"1":genpwd,"2":coded,"3":uncoded, "4":init, "5":save ,"6":exit}
        try: # essayer de lancer la fonction en utilisant le choix
            result=maindict[choix]()
        except KeyError:
            print('\033[31m' + "Option non prise en charge" + '\033[0m')
            continue
        except AssertionError:
            print('\033[31m' + "Entrez le non du fichier avec l'extantion json " + '\033[0m')
            continue
        # afficher le resulter de l'oppération
        print (f"Le resultat de votre opération est :: \033[32m {result} \033[0m")

if __name__ =="__main__":
    prc()
