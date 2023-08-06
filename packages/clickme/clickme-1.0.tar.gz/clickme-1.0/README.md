
## Introduction

This package helps to integrate [click.uz](http://click.uz) and your application is built on [django](https://www.djangoproject.com/).

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install.

```bash
pip install requests
pip install djangorestframework
pip install clickme
```

## Usage

```python
# settings.py

INSTALLED_APPS = [
     ... 
    'clickme',
    'rest_framework',
     ...
]

CLICKME_SETTINGS = {
    'ENDPOINT':'https://api.click.uz/v2/merchant/',
    'MERCHANT_ID':'',
    'SERVICE_ID':'',
    'MERCHANT_USER_ID':'',
    'SECRET_KEY':'',
}

# urls.py

urlpatterns = [
    ...
    path('api/clickme/',include('clickme.urls'))
]
```

## Get started
```bash
python manage.py migrate
python manage.py runserver
```
So now we have new API endpoint, which is ```/api/clickme/```.


## Documentation
 - [docs.click.uz](https://docs.click.uz/)
 - django-rest-framework [docs](https://www.django-rest-framework.org/)
