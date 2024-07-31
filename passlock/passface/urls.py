from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('genpass', views.genpass , name="genpass"),
    path('encod', views.encod, name="encod"),
    path('decod', views.decod, name="decod"),
    path('openfil', views.openfil, name="openfil"),
    path('managefil', views.managefil, name="managefil"),
    path('addata', views.addata, name="addata"),
    path('editdata', views.editdata, name="editdata")
]
