from django.shortcuts import render, redirect
from apps.boutique.models import Categorie, Detailvente, Produit


def panneau_vente(request):
    liste_categorie = Categorie.objects.all()
    return render (request, "cfboutik/accueil.html", {"data": liste_categorie})

def produits_par_categorie(request, categorie_id):
    categorie = Categorie.objects.get(id=categorie_id)
    liste_produits = categorie.produits.all()  # ✅ Ajoute "categorie."
    return render(request, "cfboutik/produits.html", {"produits": liste_produits})  # ✅ Nouveau template

def produit_detail(request, produit_id):
    #  récupérer le produit
    produit = Produit.objects.get(id=produit_id)
    #  retourner le render avec le bon template
    return render(request, "cfboutik/produits_details.html", {"produits détails": produit})