import encode
import decode
import json
from tabulate import tabulate


class File:
    """ Cette Classe s'occupe du fichier json et de gérer les mots de passes 
    qui y sont sauvegardés à l'aide des modules suivants:
    
    f_list: affiche un tableau contenant les données décrypter
        json2list: convertie un objet json en list
    f_init: cré un nouveau fichier de sauvegarde
    f_open: ouvre un fichier de sauvegarde existant
    f_add: ajoute des données au fichier en parammètre
    f_mod: modifi un mot de passe dans le fichier
      """
    
    def __init__(self, fichier:str, key:str) -> None:
        """
        le constructeur de notre classe

        Args:
            fichier (str): le chemin du fichier
            key (str): la clé de chiffrement du fichier

        """
       
        self.fichier = fichier
        self.key = key

    def json2list(self, dictJsn):
        """
        conversion d'un dictionnaire en liste

        Args:
            dictJsn (dict): le dictionnaire à convertir

        """
    
        liste = dictJsn["data"]
        liste = [list(liste[i].values()) for i in range(len(liste))]
        liste.insert(0, ["Index" , "Nom du site", "Identifiant (pseudo, e-mail ou numéro)", "Mot de passe"])
        return liste


    def f_list(self):
        """
        affichage des données contenues dans le fichier

        """
      
        with open(self.fichier, "r+") as f:
            dico = json.load(f)
        f_reader = self.json2list(dico)
        c= 0
        tem=[]
        for ligne in f_reader:
            if c != 0:
                dec = decode.Decoder(ligne[3],self.key)
                ligne[3] = dec.crypt()
            
            tem.append(ligne)
            c+=1
        print(tabulate(tem, tablefmt="rounded_grid", maxcolwidths=[None,None,15, 20], stralign="center"))

    def f_compt(self):
        """
        fonction pour compter le nombre d'index dans le fichier

        """
        
        with open(self.fichier, "r+") as f:
            dico = json.load(f)
            return len(dico["data"])

    def f_init(self):
        """
        fonction pour ouvrir et créer un nouveau fichier

        """
        # initier un nuveau fichier json 
        with open(self.fichier, "w") as f:
            json.dump({"data":[]}, f)
        print("\033[32m"+"fichier créer avec succès"+" \033[0m")
        return self.fichier

    def f_open(self):
        """
        fonction pour ouvrir un fichier exixtant
        """
        # ouvrir un fichier json
        self.f_list()
        return self.fichier

    def f_add(self, data:list):
        """
        fonction pour ajouter des données au fichier
        """
        dat ={}
        cles = [
            "Index" ,
            "Nom du site",
            "Identifiant (pseudo, e-mail ou numéro)",
            "Mot de passe"
            ]
        for i in range(len(data)):
            dat[cles[i]] = data[i]
        
        with open(self.fichier, "r+") as f:
            dico = json.load(f)
            dico["data"].append(dat)
        with open(self.fichier, "w+") as f:
            json.dump(dico, f)
        self.f_list()

    def f_mod(self, index:str, mdp:str):
        """
        fonction pour modifier les données d'un fichier
        """
        with open(self.fichier, "r+") as f:
            dico = json.load(f)
            lignes = dico["data"]
            enc = encode.Encoder(mdp, self.key)
            lignes[int(index)]["Mot de passe"] = enc.crypt()
                                    
        with open(self.fichier, "w+") as f:
            json.dump({"data": lignes}, f)

    def d_del(self, index:str):
        """
            fonction pour supprimer une donnée d'un fichier
        """
        with open(self.fichier, "r+") as f:
            dico = json.load(f)
            lignes = dico["data"]
            lignes.remove(lignes[int(index)])
        with open(self.fichier, "w+") as f:
            json.dump({"data": lignes}, f)



if __name__ == "__main__":
    fic =File("save.json","passck")
    fic.d_del(0)
    print(fic.f_compt())
