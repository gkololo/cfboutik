from django.shortcuts import render, redirect
from apps.boutique.models import Categorie


def panneau_vente(request):
    liste_categorie = Categorie.objects.all()
    return render (request, "cfboutik/accueil.html", {"data": liste_categorie})