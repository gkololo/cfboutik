from django.shortcuts import render, redirect
from apps.boutique.models import Categorie, Produit


def panneau_vente(request):
    liste_categorie = Categorie.objects.all()
    return render (request, "cfboutik/accueil.html", {"data": liste_categorie})

def produits_par_categorie(request, categorie_id):
    categorie = Categorie.objects.get(id=categorie_id)
    liste_produits = categorie.produits.all()  # ✅ Ajoute "categorie."
    return render(request, "cfboutik/produits.html", {"produits": liste_produits})  # ✅ Nouveau template