from django.db import models
from django.contrib.auth.models import User



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


class Vente(models.Model):
    """
    Modèle représentant une vente/transaction complète
    """
    STATUT_CHOICES = [
        ("attente", "En attente"),
        ("cloture", "Clôturée"),
        ("archive", "Archivée"),
    ]

    # Informations principales
    vendeur = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='ventes',
        help_text="Vendeur qui a effectué la transaction"
    )
    date_creation = models.DateTimeField(
        auto_now_add=True,
        help_text="Date et heure de création de la vente"
    )
    date_cloture = models.DateTimeField(
        null=True,
        blank=True,
        help_text="Date et heure de clôture de la vente"
    )

    # État de la vente
    statut = models.CharField(
        max_length=10,
        choices=STATUT_CHOICES,
        default="attente",
        help_text="État actuel de la vente"
    )

    # Informations financières
    total = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0.00,
        help_text="Montant total de la vente en euros"
    )

    # Métadonnées
    date_modification = models.DateTimeField(auto_now=True)

    def __str__(self):
        """Représentation textuelle de la vente"""
        return f"Vente #{self.id} - {self.vendeur.username} - {self.date_creation.strftime('%d/%m/%Y %H:%M')}"

    def calculer_total(self):
        """Calcule le total de la vente à partir des lignes"""
        total = sum(ligne.sous_total() for ligne in self.lignes.all())
        return total

    def nombre_articles(self):
        """Retourne le nombre total d'articles dans la vente"""
        return sum(ligne.quantite for ligne in self.lignes.all())

    def cloturer(self):
        """Clôture la vente et met à jour le total"""
        from django.utils import timezone
        self.total = self.calculer_total()
        self.statut = "cloturée"
        self.date_cloture = timezone.now()
        self.save()

    class Meta:
        verbose_name = "Vente"
        verbose_name_plural = "Ventes"
        ordering = ['-date_creation']  # Plus récentes en premier
        indexes = [
            models.Index(fields=['vendeur', 'date_creation']),
            models.Index(fields=['statut']),
        ]
class Detailvente(models.Model):
    vente = models.ForeignKey(Vente, on_delete=models.CASCADE, related_name='details')
    produit = models.ForeignKey(Produit, on_delete=models.PROTECT, related_name='produits_vendus')
    quantite = models.PositiveIntegerField(
        default=1,
        help_text= "quantité vendue")
    prix_unitaire = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text="Prix unitaire au moment de la vente"
    )

    def sous_total(self):
    #  retourne quantite × prix_unitaire
        return self.quantite * self.prix_unitaire