from django.shortcuts import render
from django.http import HttpResponse


# Create your views here.
def index(request):
    return HttpResponse("index")

def genpass(request):
    return HttpResponse("génératin de mot de pass")

def encod(request):
    return HttpResponse("encode")

def decod(request):
    return HttpResponse("encode")

def openfil(request):
    return HttpResponse("ouvrir")

def managefil(request):
    return HttpResponse("gérer")

def addata(request):
    return HttpResponse("ajout")

def editdata(request):
    return HttpResponse("modif")
