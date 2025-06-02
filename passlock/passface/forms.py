from django import forms 

class GenForm(forms.Form):
    taille = forms.IntegerField(widget=forms.NumberInput(attrs={ "min": 1, "max": 100}), initial=12)
    caractere_ascii = forms.BooleanField(required= False, widget=forms.CheckboxInput(attrs={"class": "checkbox checkbox-primary"}))
    chiffre = forms.BooleanField(required= False, initial='off', widget=forms.CheckboxInput(attrs={"class": "checkbox checkbox-primary"}))
    caractere_speciaux = forms.BooleanField(required= False, initial='off', widget=forms.CheckboxInput(attrs={"class": "checkbox checkbox-primary"}))


class EncForm(forms.Form):
    chaine = forms.CharField()
    clef = forms.CharField(widget=forms.PasswordInput)


class OpenewForm(forms.Form):
    nom_du_coffre = forms.CharField(max_length=26)
    clef = forms.CharField(widget=forms.PasswordInput)

class OpenoldForm(forms.Form):
    nom_du_coffre = forms.CharField(max_length=26)
    emplacement_du_coffre = forms.FileField(widget=forms.FileInput(attrs={'class': 'file-input'}))
    clef = forms.CharField(widget=forms.PasswordInput)

class AddForm(forms.Form):
    nom_du_site = forms.CharField()
    identifiant = forms.CharField()
    mot_de_passe = forms.CharField(widget=forms.PasswordInput, initial='booom')

class AdForm(forms.Form):
    nom_du_site = forms.CharField()
    identifiant = forms.CharField()

class ModForm(forms.Form):
    nouveau_mot_de_passe = forms.CharField(widget=forms.PasswordInput)
    
