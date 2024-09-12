from django.contrib import admin
from django.urls import path


from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('genpass', views.genpass , name="genpass"),
    path('encod', views.encod, name="encod"),
    path('decod', views.decod, name="decod"),
    path('openfil', views.openfil, name="openfil"),
    path('openoldfil', views.openoldfil, name = 'openoldfil'),
    path('managefil', views.managefil, name="managefil"),
    path('addata', views.addata, name="addata"),
    path('editdata', views.editdata, name="editdata"),
    path('download', views.download, name="download"),
    path('exited', views.exited, name="exited"),
    path('deldata', views.deldata, name="deldata")
]
