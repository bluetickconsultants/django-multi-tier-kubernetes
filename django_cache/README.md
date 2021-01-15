# Django-Cache
Using redis and django-redis to perform caching for the django application

In this tutorial we will be setting up [Redis]() and [Django] using [django-redis] and 
enable caching for our django web application.

Caching refers to storing the server response in the client itself, so that a client need 
not make a server request for the same resource again and again. A server response should 
have information about how caching is to be done, so that a client caches the response 
for a time period or never caches the server response.

## Installation
First of all install [Redis](https://redis.io/download) from the official website if 
using linux then install using the below commands or follow the instructions given on the 
[website](https://redis.io/download)

```
# command to install
Make Sure redis URL is correct.
```

## Project Setup
**start django project**
```
django-admin startproject django_cache
```

**run migrations and server**
```
python3 manage.py migrate
python3 manage.py runserver
```

**start app store**
```
python3 manage.py startapp store
```

**Configure project settings**

```
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # django apps
    'store',

    # packages
    'rest_framework',
]
```

To start using **django-redis**, you should change your Django cache settings to 
something like this:

```
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/1",  // This is the URL
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}
```

Configure as **session backend**:

```
SESSION_ENGINE = "django.contrib.sessions.backends.cache"
SESSION_CACHE_ALIAS = "default"
```

For complete code for django checkout the project files.

## [loadtest](https://www.npmjs.com/package/loadtest)
Install loadtest using npm


```
npm install -g loadtest
```

**Don't forget to run django server before running loadtest command as well as redis-server**:

```
# run these commands from separate terminals or command prompts
python manage.py runserver
redis-server
```

Run the below command to test the performance of our application
```
# command that runs 1000 requests with -k = keep connection alive and the url at last
loadtest -n 1000 -k  http://localhost:8000/store/

# output
INFO Target URL:          http://127.0.0.1:8000/store/
...
INFO Max requests:        1000
...
INFO Completed requests:  100
...
INFO Requests per second: 41
...
```

Check your terminal for more detailed results from loadtest command.

## Cached View

```
from django.shortcuts import render
from django.core.cache import cache
from django.conf import settings
from django.core.cache.backends.base import DEFAULT_TIMEOUT

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .models import Product

CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)
...

# view for cached products
@api_view(['GET'])
def view_cached_products(request):
	if 'product' in cache:
		products = cache.get('product')
		return Response(data=products, status=status.HTTP_201_CREATED)
	else:
		products = Product.objects.all()
		results = [product.to_json() for product in products]

		# store products in cache
		cache.set('product', results, timeout=CACHE_TTL)
		return Response(data=results, status=status.HTTP_201_CREATED)
```

The code above will check if the key product is present in the cache, and if found, the 
data represented will be returned to the browser. In the event that no data is present 
in the cache, we first retrieve the data from the database, store it in the cache, and 
then return the data queried to the browser.

Now that we have cached our view we can carry our tests again but this time with cached view.

```
loadtest -n 1000 -k http://127.0.0.1:8000/store/cache

# increased number of requests per second
INFO Requests per second: 248
```

The first time you hit the endpoint localhost:8000/store/cache, the application will 
query from the database and return data, but subsequent calls to the URL will bypass the 
database and query from the cache since the data is already available in the cache.

You can check if the key ```'product'``` is stored in cache or not by

```
python manage.py shell

# import cache and get the 'product' key
from django.core.cache import cache
cache.get('product')

# output
[{'name': 'hedphones',
  'description': 'best audio with non blocking IO',
  'price': '49.99',
  'timestamp': '2018-10-17 03:53:56.850768+00:00',
  'updated': '2018-10-17 03:53:56.850768+00:00'}]
```

Try increasing the number of requests in loadtest and testing out the cached django 
application.
