from django.shortcuts import render
from django.http import HttpResponse

import passmanage.encode
import passmanage.main
from .forms import *
import passmanage


# Create your views here.
def index(request):

    return render(request, 'index.html')

def genpass(request):
    if request.method == 'POST':
        form = GenForm(request.POST)
        if form.is_valid():
            try:
                request.POST['caractere_ascii']
                ascii = 'on'
            except:
                ascii = None

            try:
                request.POST['caractere_speciaux']
                symb = 'on'
            except:
                symb = None

            try:
                request.POST['chiffre']
                num = 'on'
            except:
                num = None        
            passw = passmanage.main.genere(request.POST['taille'], ascii, symb, num)
            print(passw)
    else:
        form = GenForm()
        passw = ""
    context = {'form': form, 'pass': passw}        
    return render(request, 'genpass.html', context)


def encod(request):
    
    if request.method == 'POST':
        form = EncForm(request.POST)
        if form.is_valid():
            mot = request.POST['chaine']
            cle = request.POST['clef']
            chiffreur = passmanage.encode.Encoder(mot,cle)
            result = chiffreur.crypt()
            
    else:
        form = EncForm()
        result = ''
    context= {'form' : form, 'result': result}        
    return render(request, 'encod.html', context)

def decod(request):
    
    if request.method == 'POST':
        form = EncForm(request.POST)
        if form.is_valid():
            mot = request.POST['chaine']
            cle = request.POST['clef']
            chiffreur = passmanage.decode.Decoder(mot,cle)
            result = chiffreur.crypt()
            
    else:
        form = EncForm()
        result = ''
    context= {'form' : form, 'result': result}        
    return render(request, 'decod.html', context)
def openfil(request):
    return HttpResponse("ouvrir")

def managefil(request):
    return HttpResponse("gérer")

def addata(request):
    return HttpResponse("ajout")

def editdata(request):
    return HttpResponse("modif")
