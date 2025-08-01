from django.contrib import admin
from .models import Categorie, Produit

@admin.register(Categorie)
class CategorieAdmin(admin.ModelAdmin):
    list_display = ('nom', 'parent', 'couleur')
    list_filter = ('parent',)
    search_fields = ('nom', 'description')

@admin.register(Produit)
class ProduitAdmin(admin.ModelAdmin):
    list_display = ('nom', 'prix_vente', 'prix_libre', 'stock_actuel', 'gestion_stock', 'actif')
    list_filter = ('actif', 'gestion_stock', 'prix_libre', 'categories')
    search_fields = ('nom', 'code_sku', 'description')
    filter_horizontal = ('categories',)