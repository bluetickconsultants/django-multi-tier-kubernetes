from django.urls import path

from .views import view_products, view_cached_products

app_name = 'store'

urlpatterns = [
	path('', view_products, name='products'),
	path('cache/', view_cached_products, name='cached-products'),
]
