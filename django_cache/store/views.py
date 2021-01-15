from django.shortcuts import render
from django.core.cache import cache
from django.conf import settings
from django.core.cache.backends.base import DEFAULT_TIMEOUT

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .models import Product

CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)

@api_view(['GET'])
def view_products(request):
	products = Product.objects.all()
	results = [product.to_json() for product in products]
	return Response(data=results, status=status.HTTP_201_CREATED)


# view for cached products
@api_view(['GET'])
def view_cached_products(request):
	if 'product' in cache:
		print("True")
		products = cache.get('product')
		return Response(data=products, status=status.HTTP_201_CREATED)
	else:
		print("False")
		products = Product.objects.all()
		results = [product.to_json() for product in products]

		# store products in cache -> ('key', 'value', timeout)
		cache.set('product', results, timeout=CACHE_TTL)
		return Response(data=results, status=status.HTTP_201_CREATED)
