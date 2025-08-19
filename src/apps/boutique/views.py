from django.contrib import messages
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
    return render(request, "cfboutik/produit_detail.html", {"produit": produit})


def ajouter_panier(request, produit_id):
    if request.method == 'POST':  # ← D'ABORD vérifier si POST
        try:
            quantite = int(request.POST.get('quantite', 1))

            if quantite <= 0:
                raise ValueError("Quantité invalide")

            produit = Produit.objects.get(id=produit_id)

            # Vérifier le stock SEULEMENT si gestion activée
            if produit.gestion_stock and quantite > produit.stock_actuel:
                raise ValueError("Stock insuffisant")

            # ✅ ICI récupérer le panier (après validation)
            categorie = produit.categories.first()          #prendre l'instance categorie
            panier = request.session.get('panier', {})

            produit_id_str = str(produit_id)

            if produit_id_str in panier:
                panier[produit_id_str]['quantite'] += quantite
            else:
                panier[produit_id_str] = {
                'quantite': quantite,
                'prix': float(produit.prix_vente),
                'categorie_id': categorie.id,  # ← Stocker la catégorie !
                'nom_produit': produit.nom     # ← Bonus : nom pour affichage
}

            request.session['panier'] = panier
            return redirect('produits', categorie_id=categorie.id)   #retour à la catégorie pour meilleure UX

        except (ValueError, Produit.DoesNotExist):
            messages.error(request, "Erreur dans les données")
            return redirect('produit_detail', produit_id=produit_id)


    # Si pas POST, rediriger
    return redirect('produits_par_categorie')

