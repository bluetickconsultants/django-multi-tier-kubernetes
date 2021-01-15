from django.contrib import admin

from .models import Product

@admin.register(Product)
class ProductModelAdmin(admin.ModelAdmin):
	list_display = ('name', 'price', 'timestamp')
	search_fields = ('name', 'price', 'timestamp', 'updated')
	list_filter = ('timestamp', 'updated')
