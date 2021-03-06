"""
Django settings for boutique project.

Generated by 'django-admin startproject' using Django 3.1.5.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""
import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'fto$((q+4hf6a&%wi-@^&)6q=ri0c5@fwq0(bfi-r26lm5#lhg'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # used by the social account app to create the proper callback URLs
    # when connecting via social media accounts.
    'django.contrib.sites',
    'allauth',
    # allauth app that allows the basic user account stuff
    # like logging in and out. User registration and password resets.
    'allauth.account',
    # handles logging in via social media providers like Facebook and Google
    'allauth.socialaccount',
    'home',
    'products',
    'bag',
    'checkout',

    # Other
    'crispy_forms'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'boutique.urls'

CRISPY_TEMPLATE_PACK = 'bootstrap4'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates'),
            os.path.join(BASE_DIR, 'templates', 'allauth')
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                # required by allauth, it allows allauth and django access the
                # HTTP request object in our templates. i.e. we want access
                # request.user or request.user.email in our django templates
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                # access the no image file in the media folder if a product
                # doesn't have an image.
                'django.template.context_processors.media',
                # anytime we need to access the bag contents in any template
                # across the entire site they'll be available to us without
                # having to return them from a whole bunch of different views
                # acrossdifferent apps.
                'bag.contexts.bag_contents'
            ],
            # add a list called built-ins which will contain all the tags we
            # want available in all our templates by default from
            # crispy_forms.template_tags we want to add both crispy_forms_tags
            # and crispy_forms_field.
            'builtins': [
                'crispy_forms.templatetags.crispy_forms_tags',
                'crispy_forms.templatetags.crispy_forms_field',
            ]
        },
    },
]
# tell it to store messages in the session this is often not a required step
# because there is a default which falls back to this storage method but due
# to the use of git pod in these recordings it's require
MESSAGE_STORAGE = 'django.contrib.messages.storage.session.SessionStorage'

# Allow users to log into our store via their email address which at the time
# still isn't supported by default in django.
AUTHENTICATION_BACKENDS = [
    # Needed to login by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend',

    # `allauth` specific authentication methods, such as login by e-mail
    'allauth.account.auth_backends.AuthenticationBackend',
]

# used by the social account app to create the proper callback URLs
# when connecting via social media accounts.
SITE_ID = 1

# Temporarily log emails to the console so we can get the confirmation links.
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# tells allauth that we want to allow authentication using either
# usernames or emails
ACCOUNT_AUTHENTICATION_METHOD = 'username_email'
# make it so that an email is required to register for the site.
ACCOUNT_EMAIL_REQUIRED = True
# Verifying your email is mandatory so we know users are using a real email.
ACCOUNT_EMAIL_VERIFICATION = 'mandatory'
# required to enter their email twice on the registration page
# to make sure that they haven't made any typos.
ACCOUNT_SIGNUP_EMAIL_ENTER_TWICE = True
ACCOUNT_USERNAME_MIN_LENGTH = 4
# specifying a login url and a url to redirect back to after logging in.
LOGIN_URL = '/accounts/login/'
LOGIN_REDIRECT_URL = '/'

WSGI_APPLICATION = 'boutique.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

# tell Django where all of our static files are located.
# Since they're located in the project level static folder.
# All we need to do is os.path.join(BASE_DIR, 'static')
# although normally we would also want to supply a static route
# setting here for Django's collectstatic utility to work.I'm not going
# to do that because it will interfere with setting up AWS later on
STATIC_URL = '/static/'
STATICFILES_DIRS = (os.path.join(BASE_DIR, 'static'),)

# to allow Django to see the MEDIA_URL. We need to go to urls.py
# Import our settings and the static function from django.conf.urls.static
# And use the static function to add the MEDIA_URL to our list of URLs.
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# add 2 new variables which will be used to calculate delivery costs
FREE_DELIVERY_THRESHOLD = 50
STANDARD_DELIVERY_PERCENTAGE = 10

# Stripe
STRIPE_CURRENCY = 'usd'
STRIPE_PUBLIC_KEY = os.getenv('STRIPE_PUBLIC_KEY', '')
STRIPE_SECRET_KEY = os.getenv('STRIPE_SECRET_KEY', '')
STRIPE_WH_SECRET = os.getenv('STRIPE_WH_SECRET', '')
