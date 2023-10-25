

import encode
import decode
import csv
from tabulate import tabulate

def f_list(fichier, key):
    """
    affichage du contenus de la sauvegarde comme un tableau

    Args:
        fichier (str): nom du fichier
        key (str): clé de chiffrement

    """
    with open(fichier, "r") as f:
        f_reader = list(csv.reader(f))
        c= 0
        tem=[]
        for ligne in f_reader:
            if c != 0:
                ligne[3] = decode.crypt(ligne[3],key)
            
            tem.append(ligne)
            c+=1

        print(tabulate(tem, tablefmt="rounded_grid", maxcolwidths=[None,None,15, 20], stralign="center"))

def f_compt(fichier):
    """
    retourne le dernier index du tableau

    Args:
        fichier (str):nom du fichier

    """
    with open(fichier, "r") as f:
        f_reader = csv.reader(f)
        return len(list(f_reader))

def f_init(fichier):
    """
    initialisation d'un nouveau fichier

    Args:
        fichier (str):nom du fichier

    """
    # initier un nuveau fichier csv et un nouvel objet csv
    with open(fichier, "w") as f:
        f_writer = csv.writer(f)
    
        # ajouter les titres 
        f_writer.writerow([
        "Index" ,
        "Nom du site",
        "Identifiant (pseudo, e-mail ou numéro)",
        "Mot de passe"
        ])
    print("\033[32m"+"fichier créer avec succès"+" \033[0m")
    return fichier

def f_open(fichier:str, key:str):
    """
    simuler l'ouverture d'un fichier en utilisant la fonction f_list

    Args:
        fichier (str):nom du fichier
        key (str): la clé  du fichier  

    """
    # ouvrir un fichier csv et un objet csv
    f_list(fichier, key)
    return fichier

def f_add(fichier:str, data:list, key:str):
    """
    ajouter des donnée au fichier

    Args:
        fichier (str):nom du fichier
        data (list): données a ajouter
        key (str):la clé  du fichier

    """
    with open(fichier, "a") as f:
        f_writer = csv.writer(f)
        f_writer.writerow(data)
    f_list(fichier, key)

def f_mod(fichier:str, index:str, mdp:str, key:str):
    """
    modifier un mot de passe dans le fichier

    Args:
        fichier (str):nom du fichier
        index (str): l'index du mot de passe à modifier
        mdp (str): le mot de passe à modifier
        key (str):la clé  du fichier

    """
    with open(fichier, "r") as f:
        f_reader = csv.reader(f)
        lignes = list(f_reader)
        for i in range(len(lignes)):
            if lignes[i][0] == index:
                lignes[i][3] = encode.crypt(mdp, key)
                                
    with open(fichier, "w") as f:
        f_writer = csv.writer(f)
        f_writer.writerows(lignes)

if __name__ == "__main__":    
    print(f_compt("cool.csv"))
