from django.contrib import admin
from .models import Product, Operation

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'quantity', 'unit', 'price')
    search_fields = ('name',)
    
@admin.register(Operation)
class OperationAdmin(admin.ModelAdmin):
    list_display = ('number','date', 'doc_date', 'type', 'counterparty', 'storage_location')
    search_fields = ('type',)
