# Django RestFull API
A Django RestFull API for Bills App.

## Django
```
# Python Packages to install
pip install Django
pip install djangorestframework
pip install djangorestframework-simplejwt
pip install django-cors-headers
```

```
# Create the Project.
django-admin startproject jwttoken
```

```
# Create the app.
python manage.py startapp authentication
```

```python
#  setting.py

.....
INSTALLED_APPS = [
     ...........
     'authentication',
     'corsheaders',
     'rest_framework',
     'rest_framework_simplejwt.token_blacklist'
]

.....
CORS_ORIGIN_ALLOW_ALL = True
.....

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    ...........
]
.....

REST_FRAMEWORK = {
     'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
      ],
}
.....

SIMPLE_JWT = {
     'ACCESS_TOKEN_LIFETIME': timedelta(minutes=10),
     'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
     'ROTATE_REFRESH_TOKENS': True,
     'BLACKLIST_AFTER_ROTATION': True
}
```
1. **CORS_ORIGIN_ALLOW_ALL = True:**
This setting enables Cross-Origin Resource Sharing (CORS) for all origins. It allows requests from any origin to access the Django application's resources. CORS is a security mechanism that restricts cross-origin requests, and by setting this to True, all origins are allowed to make requests to the Django application. This can be useful when developing APIs that need to be accessed by different clients from different domains.

2. **MIDDLEWARE with 'corsheaders.middleware.CorsMiddleware':**
This code snippet adds the CorsMiddleware to the list of middlewares used by Django. Middleware in Django is a way to process requests and responses globally before they reach the view or after they leave the view. The CorsMiddleware handles CORS-related headers and allows cross-origin requests by adding the necessary headers to the responses.

3. **REST_FRAMEWORK with 'DEFAULT_AUTHENTICATION_CLASSES':**
This setting configures the Django REST Framework to use JWT authentication as the default authentication class. By specifying 'rest_framework_simplejwt.authentication.JWTAuthentication' in the DEFAULT_AUTHENTICATION_CLASSES setting, it instructs the framework to use JWT tokens for authenticating requests. This ensures that all API endpoints are protected and require a valid JWT token for access.

