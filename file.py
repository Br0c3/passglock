import encode
import decode
import csv
import json
from tabulate import tabulate

class file():
    
    def __init__(self, fichier, key) -> None:
       
        self.fichier = fichier
        self.key = key

    def list2json(self, listes : list):
        temp = []

        for liste in listes:
            dico ={}
            cles = [
            "Index" ,
            "Nom du site",
            "Identifiant (pseudo, e-mail ou numéro)",
            "Mot de passe"
            ]
            for i in range(len(liste)):
                dico[cles[i]] = liste[i]

            temp.append(dico)
        
        return {"data": temp}
    
    def json2list(self, dictJsn):

        liste = dictJsn["data"]
        liste = [list(liste[i].values()) for i in range(len(liste))]
        liste.insert(0, ["Index" , "Nom du site", "Identifiant (pseudo, e-mail ou numéro)", "Mot de passe"])
        return liste


    def f_list(self):
      
        with open(self.fichier, "r+") as f:
            dico = json.load(f)
        f_reader = self.json2list(dico)
        c= 0
        tem=[]
        for ligne in f_reader:
            if c != 0:
                dec = decode.decoder(ligne[3],self.key)
                ligne[3] = dec.crypt()
            
            tem.append(ligne)
            c+=1
        print(tabulate(tem, tablefmt="rounded_grid", maxcolwidths=[None,None,15, 20], stralign="center"))

    def f_compt(self):
        
        with open(self.fichier, "r+") as f:
            dico = json.load(f)
            return len(dico["data"])

    def f_init(self):
        
        # initier un nuveau fichier json 
        with open(self.fichier, "w") as f:
            json.dump({"data":[]}, f)
        print("\033[32m"+"fichier créer avec succès"+" \033[0m")
        return self.fichier

    def f_open(self):
        
        # ouvrir un fichier json
        self.f_list()
        return self.fichier

    def f_add(self, data:list):
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
        
        with open(self.fichier, "r+") as f:
            dico = json.load(f)
            lignes = dico["data"]
            enc = encode.encoder(mdp, self.key)
            lignes[int(index)]["Mot de passe"] = enc.crypt()
                                    
        with open(self.fichier, "w+") as f:
            json.dump({"data": lignes}, f)

if __name__ == "__main__":
    fic =file("save.csv","passck")
    print(fic.f_compt())
