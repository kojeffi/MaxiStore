"""
Django settings for melianSafeSysAi project.

Generated by 'django-admin startproject' using Django 5.0.4.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

import dj_database_url
import os

from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get("DEBUG", "False").lower() == "true"

ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS",'').split(" ")

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'store',
    'user_app',
    'django_bootstrap5',
    'widget_tweaks',
    'crispy_forms',
    'ml',
    'rest_framework',
	'cloudinary',
    'cloudinary_storage',

    'grappelli',
]

import os

CLOUDINARY_STORAGE = {
    'CLOUD_NAME': os.getenv('CLOUDINARY_CLOUD_NAME'),
    'API_KEY': os.getenv('CLOUDINARY_API_KEY'),
    'API_SECRET': os.getenv('CLOUDINARY_API_SECRET'),
}

DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'


CRISPY_ALLOWED_TEMPLATE_PACKS = 'bootstrap4'
CRISPY_TEMPLATE_PACK = 'bootstrap4'



# Machine learning API
ML_API_URL = os.getenv('ML_API_URL', 'http://localhost:8000/ml')


# ML_API_URL = os.getenv('ML_API_URL', 'https://maxistore.onrender.com/ml/')



# Logging Configuration
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'logs/django_error.log'),
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'ERROR',
            'propagate': True,
        },
        'ecommerce': {
            'handlers': ['file'],
            'level': 'ERROR',
            'propagate': True,
        },
    },
}

# Ensure the logs directory exists
os.makedirs(os.path.join(BASE_DIR, 'logs'), exist_ok=True)

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'ecommerceProject.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'store.context_processors.cart_items_count',
            ],
        },
    },
]


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

database_url = os.environ.get('DATABASE_URL')
if database_url:
    DATABASES["default"] = dj_database_url.parse('postgres://ecommerce_odcq_user:Mrdz1sDhXodAqUdYzb8WXkzlQwgqg0AG@dpg-cpo4o6dds78s73babkog-a.oregon-postgres.render.com/ecommerce_odcq')



# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {
            'min_length': 9,
        }
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Secure Cookies
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True

# Security settings
SECURE_BROWSER_XSS_FILTER = True
X_FRAME_OPTIONS = 'DENY'
SECURE_SSL_REDIRECT = os.getenv('SECURE_SSL_REDIRECT', 'False').lower() == 'true'
SECURE_HSTS_SECONDS = int(os.getenv('SECURE_HSTS_SECONDS', '3600'))
SECURE_HSTS_INCLUDE_SUBDOMAINS = os.getenv('SECURE_HSTS_INCLUDE_SUBDOMAINS', 'True').lower() == 'true'
SECURE_HSTS_PRELOAD = os.getenv('SECURE_HSTS_PRELOAD', 'True').lower() == 'true'



# Authentication backends
AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
)


# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


import os

# Define the URL for serving static files
STATIC_URL = '/static/'

# Define the directory where static files will be collected during deployment
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Additional directories for static files (for development purposes)
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

# Define the URL for serving media files
MEDIA_URL = '/media/'

# Define the directory where media files will be uploaded
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')



# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Email settings for Gmail SMTP
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'omondijeff88@gmail.com'
EMAIL_HOST_PASSWORD = 'ersq gtcc boga qsvd'


import os

# Define the URL for serving static files
STATIC_URL = '/static/'

# Define the directory where static files will be collected during deployment
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Additional directories for static files (for development purposes)
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

# Define the URL for serving media files
MEDIA_URL = '/media/'

# Define the directory where media files will be uploadeMEDIA_ROOT = os.path.join(BASE_DIR, 'media')

LOGIN_REDIRECT_URL = 'home-url'
LOGIN_URL = 'login-url'

LOGOUT_REDIRECT_URL = 'logout-url'



# Stripe settings
# STRIPE_PUBLIC_KEY = 'your_stripe_public_key'
# STRIPE_SECRET_KEY = 'your_stripe_secret_key'
# STRIPE_SECRET_KEY = 'sk_test_51PLPxiFYYX5YHgfBLfVEwf4vsM0AOCXRd0oyAncoYe2UeFX7q7tKdBhEi5NmAKXhqvIzMuCGqbVxzLX6AMMnvMNE00OpQFMXKZ'
# STRIPE_PUBLIC_KEY  = 'pk_test_51PLPxiFYYX5YHgfB8BnLGDZijrDmvm5shkv1aoiU8bvta8HEFgezuMexHoRmvlYnPN1Ly35o6Mrr3wUUkQemqHBq00rrFGMFwH'

# # PayPal settings
# PAYPAL_CLIENT_ID = 'ARZlIyQyoUCPoxKAzHIDsKTARpcHOvTWERandV-4YXc6A9fkIshnmBEicE5q6sjNFeBnKbesEMbl6QlK'
# PAYPAL_CLIENT_SECRET = 'EC6HkA1jkJoNOY7_3qVcNi8hXSRuq9mY3Q_a_eJqLDy-2dP34ImOhkijjG3wDjn79xk_PQR7XoKqgoTO'
# PAYPAL_MODE = 'live'  # Or 'live' for production



# Stripe settings
STRIPE_PUBLIC_KEY = os.getenv('STRIPE_PUBLIC_KEY')
STRIPE_SECRET_KEY = os.getenv('STRIPE_SECRET_KEY')

# PayPal settings
PAYPAL_CLIENT_ID = os.getenv('PAYPAL_CLIENT_ID')
PAYPAL_CLIENT_SECRET = os.getenv('PAYPAL_CLIENT_SECRET')
PAYPAL_MODE = os.getenv('PAYPAL_MODE', 'live')  # Default to 'live' if not set


# machine Learning

# Machine Learning Data Settings

# User-item interaction data
USER_ITEM_INTERACTIONS = [
    {"user_id": 1, "item_id": 101, "interaction": 5},
    {"user_id": 2, "item_id": 102, "interaction": 3},
    {"user_id": 1, "item_id": 103, "interaction": 2},
    {"user_id": 3, "item_id": 101, "interaction": 4},
    {"user_id": 2, "item_id": 104, "interaction": 1},
]

# Historical prices of products
HISTORICAL_PRICES = [
    {"product_id": 101, "competitor_price": 20.5},
    {"product_id": 102, "competitor_price": 22.0},
    {"product_id": 103, "competitor_price": 18.0},
    {"product_id": 104, "competitor_price": 21.5},
]

# Demand data for products
DEMAND_DATA = [
    {"product_id": 101, "demand": 100, "date": "2024-01-01"},
    {"product_id": 102, "demand": 150, "date": "2024-01-02"},
    {"product_id": 103, "demand": 80, "date": "2024-01-03"},
    {"product_id": 104, "demand": 60, "date": "2024-01-04"},
    {"product_id": 101, "demand": 120, "date": "2024-01-05"},
]

# Customer demographic data
CUSTOMER_DATA = [
    {"customer_id": 1, "age": 25, "income": 50000, "spending_score": 60},
    {"customer_id": 2, "age": 30, "income": 60000, "spending_score": 70},
    {"customer_id": 3, "age": 22, "income": 45000, "spending_score": 50},
    {"customer_id": 4, "age": 35, "income": 70000, "spending_score": 80},
    {"customer_id": 5, "age": 28, "income": 52000, "spending_score": 65},
]

# Customer features
CUSTOMER_FEATURES = [
    {"customer_id": 1, "feature_1": 0.1, "feature_2": 0.8},
    {"customer_id": 2, "feature_1": 0.2, "feature_2": 0.9},
    {"customer_id": 3, "feature_1": 0.3, "feature_2": 0.7},
    {"customer_id": 4, "feature_1": 0.4, "feature_2": 0.6},
    {"customer_id": 5, "feature_1": 0.5, "feature_2": 0.5},
]

# Customer churn target (binary classification)
CUSTOMER_CHURN_TARGET = [0, 1, 0, 1, 0]

# Transaction data
TRANSACTION_DATA = [
    {"transaction_id": 1, "amount": 100.0, "fraud": 0},
    {"transaction_id": 2, "amount": 150.0, "fraud": 1},
    {"transaction_id": 3, "amount": 200.0, "fraud": 0},
    {"transaction_id": 4, "amount": 250.0, "fraud": 1},
    {"transaction_id": 5, "amount": 300.0, "fraud": 0},
]

# Reviews for products
REVIEWS = [
    "Great product, very satisfied.",
    "Not what I expected, quite disappointed.",
    "Average quality, could be better.",
    "Excellent value for money.",
    "Terrible experience, will not buy again.",
]

# Purchase history of users
PURCHASE_HISTORY = [
    {"user_id": 1, "items": ["item_101", "item_102"]},
    {"user_id": 2, "items": ["item_103"]},
    {"user_id": 3, "items": ["item_104", "item_101"]},
    {"user_id": 4, "items": ["item_102", "item_103"]},
    {"user_id": 5, "items": ["item_101", "item_104"]},
]

# User preferences
USER_PREFERENCES = {
    1: "electronics",
    2: "books",
    3: "fashion",
    4: "home appliances",
    5: "toys",
}

# User behavior on items
USER_BEHAVIOR = [
    {"user_id": 1, "action": "click", "item_id": 101},
    {"user_id": 2, "action": "view", "item_id": 102},
    {"user_id": 3, "action": "purchase", "item_id": 103},
    {"user_id": 4, "action": "click", "item_id": 104},
    {"user_id": 5, "action": "view", "item_id": 101},
]

# Search results for products
SEARCH_RESULTS = [
    {"product_id": 101, "features": [0.1, 0.2, 0.3]},
    {"product_id": 102, "features": [0.2, 0.3, 0.4]},
    {"product_id": 103, "features": [0.3, 0.4, 0.5]},
    {"product_id": 104, "features": [0.4, 0.5, 0.6]},
    {"product_id": 105, "features": [0.5, 0.6, 0.7]},
]
