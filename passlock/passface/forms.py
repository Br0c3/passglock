from django import forms 

class GenForm(forms.Form):
    taille = forms.IntegerField(25,6,True)
    caractere_ascii = forms.CheckboxInput()
    chiffre = forms.CheckboxInput()
    caractere_speciaux = forms.CheckboxInput()


class EncForm(forms.Form):
    chaine = forms.CharField(300)
    clef = forms.PasswordInput()


class openForm(forms.Form):
    coffre = forms.FileField()
    clef = forms.PasswordInput()


class AddForm(forms.Form):
    nom_du_site = forms.CharField(300)
    identifiant = forms.CharField(50)
    clef = forms.PasswordInput()


class ModForm(forms.Form):
    index = forms.PasswordInput()
    clef = forms.PasswordInput()