from django.shortcuts import render, redirect
from django.http import HttpResponse
import jsonpickle , json
from django.contrib.auth import logout

import passmanage.encode
import passmanage.main
from .forms import *
from passmanage.file1 import File
import passmanage


def index(request):
    try:
        sessio = request.session["name"] 
    except(KeyError):
        sessio = "none"  
    return render(request, 'index.html', {"session" : sessio})

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
            request.session["name"] = fname
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
            request.session["name"] = fname
            return redirect("managefil")
    else:
        form = OpenoldForm()
    return render(request, 'openoldfil.html',{'form': form})

def managefil(request):
    try:
        flist = jsonpickle.decode(request.session["file"]).f_list()
        name = request.session["name"]
    except(KeyError):
        return redirect("index")
    return render(request, 'managefil.html', {'flist': flist, "name" : name})

def addata(request):
    if request.method == 'POST':
        form = AddForm(request.POST)
        if form.is_valid():
            fname = request.POST['nom_du_site']
            idnt = request.POST["identifiant"]
            key = request.POST["mot_de_passe"]
            try:
                finstce = jsonpickle.decode(request.session["file"])
            except(KeyError):
                return redirect("index")
        
            indx = finstce.f_compt()
            print(indx)
            finstce.f_add([indx, fname,idnt, key])
            request.session["file"] = jsonpickle.encode(finstce)
            return redirect("managefil")
    else:
        form = AddForm()
    return render(request, 'addata.html',{'form': form})

def editdata(request):
    if request.method == 'POST':
        form = ModForm(request.POST)
        if form.is_valid():
            key = request.POST["nouveau_mot_de_passe"]
            indx = request.POST["index"]
            try:
                finstce = jsonpickle.decode(request.session["file"])
            except(KeyError):
                return redirect("index")    
            
            finstce.f_mod(indx, key)

            request.session["file"] = jsonpickle.encode(finstce)
            return redirect("managefil")
    else:
        indx = request.GET["indx"]
        form = ModForm()
    return render(request, 'editdata.html',{'form': form, 'indx': indx})

def deldata(request):
    if request.method == "GET":
        try:
            finstce = jsonpickle.decode(request.session["file"])
        except(KeyError):
            return redirect("index")    
        indx = request.GET["indx"]
        finstce.f_del(indx)
        request.session["file"] = jsonpickle.encode(finstce)
    return redirect("managefil")

def download(request):
    try:
        fichier = jsonpickle.decode(request.session["file"]).fson.getvalue()
    except(KeyError):
        return redirect("index")    
    fName = request.session['name']
    mine_type = "application/json" #determiner le type de fichier a envoyer dans la reponce
    response = HttpResponse(fichier, content_type=mine_type) # construire la reponce http
    response['Content-Disposition'] = "attachement; filename= " + fName + ".json" #customiser la reponce http en ajoutant le nom du fichier 
    return response
    return HttpResponse("telecharge")

def exited(request):
    logout(request)
    return redirect(index)
