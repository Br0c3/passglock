from django import forms 

class GenForm(forms.Form):
    taille = forms.IntegerField()
    caractere_ascii = forms.BooleanField(required= False)
    chiffre = forms.BooleanField(required= False, initial='off')
    caractere_speciaux = forms.BooleanField(required= False, initial='off')


class EncForm(forms.Form):
    chaine = forms.CharField()
    clef = forms.CharField(widget=forms.PasswordInput)


class OpenewForm(forms.Form):
    nom_du_coffre = forms.CharField(max_length=26)
    clef = forms.CharField(widget=forms.PasswordInput)

class OpenoldForm(forms.Form):
    nom_du_coffre = forms.CharField(max_length=26)
    emplacement_du_coffre = forms.FileField()
    clef = forms.CharField(widget=forms.PasswordInput)

class AddForm(forms.Form):
    nom_du_site = forms.CharField()
    identifiant = forms.CharField()
    clef = forms.CharField(widget=forms.PasswordInput)


class ModForm(forms.Form):
    index = forms.PasswordInput()
    clef = forms.CharField(widget=forms.PasswordInput)
    

class DelForm(forms.Form):
    index = forms.PasswordInput()
     