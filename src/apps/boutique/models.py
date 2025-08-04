from django.db import models


# Create your models here.
class Categorie(models.Model):
    nom = models.CharField(max_length=150)
    description = models.TextField(blank=True, null=True)
    couleur = models.CharField(max_length=7, blank=True, null=True, help_text="Format: #FFFFFF")
    icone = models.CharField(max_length=50, blank=True, null=True, help_text="Nom de l'icône")
    parent = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True, related_name='enfants')

    def __str__(self):
        return self.nom

    class Meta:
        verbose_name_plural = "Catégories"


class Produit(models.Model):
    # Informations de base (garder)
    nom = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    code_sku = models.CharField(max_length=50, blank=True, null=True, unique=True)

    # Prix - VERSION FLEXIBLE
    prix_achat = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    prix_vente = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True,
                                   help_text="Prix fixe du produit (optionnel)")
    prix_libre = models.BooleanField(default=False,
                                   help_text="Autoriser la saisie d'un prix libre à la vente")

    # Image (garder)
    image = models.ImageField(upload_to='produits/', blank=True, null=True)

    # Stock (garder)
    gestion_stock = models.BooleanField(default=True)
    stock_actuel = models.PositiveIntegerField(default=0)
    stock_minimum = models.PositiveIntegerField(default=0)

    # Statut (garder)
    actif = models.BooleanField(default=True)

    # Relations (garder)
    categories = models.ManyToManyField(Categorie, related_name='produits')

    def __str__(self):
        return self.nom