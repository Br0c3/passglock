from django.shortcuts import render, redirect
from django.http import HttpResponse
import jsonpickle , json

import passmanage.encode
import passmanage.main
from .forms import *
from passmanage.file1 import File
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
    if request.method == 'POST':
        form = OpenewForm(request.POST)
        if form.is_valid():
            fname = request.POST['nom_du_coffre']
            finstce = File( request.POST["clef"])
            finstce.f_init()
            request.session["file"] = jsonpickle.encode(finstce)
            return redirect("managefil")
    else:
        form = OpenewForm()
    return render(request, 'openfil.html',{'form': form})

def openoldfil(request):
    if request.method == 'POST':
        form = OpenoldForm(request.POST, request.FILES)
        if form.is_valid():
            fname = request.POST['nom_du_coffre']
            finstce = File( request.POST["clef"], request.FILES['emplacement_du_coffre'])
            finstce.f_open()
            request.session["file"] = jsonpickle.encode(finstce)
            return redirect("managefil")
    else:
        form = OpenoldForm()
    return render(request, 'openfil.html',{'form': form})

def managefil(request):
    flist = jsonpickle.decode(request.session["file"]).f_list()
    return render(request, 'managefil.html', {'flist': flist})

def addata(request):
    return HttpResponse("ajout")

def editdata(request):
    return HttpResponse("modif")

def deldata(request):
    return HttpResponse("supprimer")

def download(request):
    return HttpResponse("telecharge")

def exited(request):
    return HttpResponse("quitter")
