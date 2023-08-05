import os
import environ
import webspace
from webspace.cms import constants
from webspace.settings import base as base_settings
import pkg_resources

BASE_DIR = os.environ['BASE_DIR']
env = environ.Env()
environ.Env.read_env(BASE_DIR + '/.env')

#  Vars

path_webspace = os.path.dirname(webspace.__file__)
DEBUG = env.bool('DEBUG', default=True)
SITE_NAME = env.str('APP_NAME', default='webspace')
DOMAINS_NAME = env.list('DOMAINS_NAME')
BUCKET_NAME = env.str('BUCKET_NAME')
BUCKET_URL = env.str('BUCKET_URL')
BUCKET_URL_CDN = env.str('BUCKET_URL_CDN')
SENDGRID_SK = env.str('SENDGRID_SK', default=None)
YANDEX_TRANSLATE_KEY = env.str('YANDEX_TRANSLATE_KEY')
DATABASES = {
    'default': env.db(
        'DATABASE',
        default='psql://postgres:password@127.0.0.1:5432/webspacedb',
    )
}
VERSION = base_settings.get_package_version(os.path.join(BASE_DIR, 'package.json'))
IS_WEBSPACE = True if SITE_NAME == 'webspace' else False
if IS_WEBSPACE:
    VERSION_WEBSPACE = VERSION
else:
    VERSION_WEBSPACE = pkg_resources.get_distribution("webspace").version


# Django

SECRET_KEY = base_settings.generate_secret_key()
SITE_ID = 1
ALLOWED_HOSTS = DOMAINS_NAME + base_settings.ALLOWED_HOSTS_DEV

INSTALLED_APPS = (['webspace.cms.apps.CmsConfig'] if IS_WEBSPACE else ['cms.apps.CmsConfig']) + base_settings.INSTALLED_APPS
MIDDLEWARE = base_settings.MIDDLEWARE
TEMPLATES = base_settings.get_templates(BASE_DIR, IS_WEBSPACE, path_webspace)
WSGI_APPLICATION = 'wsgi.application'
LOGGING = base_settings.LOGGING
DATA_UPLOAD_MAX_NUMBER_FIELDS = 10240
ROOT_URLCONF = 'urls' if IS_WEBSPACE else 'cms.urls'
LOGIN_URL = '/admin_W3cJ32mq63V45CLvmjNbsqSJ32mq63V45CL/login/'
if not DEBUG:

    """
    SECURE_HSTS_SECONDS = 50000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    SECURE_SSL_REDIRECT = True
    SECURE_REFERRER_POLICY = "same-origin"
    """

    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    os.environ['HTTPS'] = "on"
    os.environ['wsgi.url_scheme'] = "https"
    base_settings.run_sentry()


#  User

AUTH_USER_MODEL = "account.User"
AUTH_PASSWORD_VALIDATORS = base_settings.AUTH_PASSWORD_VALIDATORS

# Languages

LANGUAGE_CODE = 'fr-FR'
TIME_ZONE = 'Europe/Paris'
USE_I18N = True
USE_L10N = True
USE_TZ = True
ROSETTA_ENABLE_TRANSLATION_SUGGESTIONS = True
ROSETTA_WSGI_AUTO_RELOAD = True
ROSETTA_UWSGI_AUTO_RELOAD = True
LANGUAGES = constants.LANGUAGES
LOCALE_PATHS = [
    os.path.join(path_webspace, 'webspace/cms/locale' if IS_WEBSPACE else 'cms/locale'),
]


#  Files

STATICFILES_FINDERS = base_settings.STATICFILES_FINDERS
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')] if IS_WEBSPACE else [os.path.join(path_webspace, 'cms/static')]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATIC_URL = '/static/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'mediafiles')
MEDIA_URL = BUCKET_URL
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
DATA_UPLOAD_MAX_MEMORY_SIZE = 26214400

#  AWS

AWS_ACCESS_KEY_ID = env.str('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = env.str('AWS_SECRET_ACCESS_KEY')
AWS_S3_REGION_NAME = 'eu-west-3'
AWS_S3_CUSTOM_DOMAIN = BUCKET_URL_CDN
EMAIL_BACKEND = 'django_ses.SESBackend'
AWS_SES_REGION_NAME = 'eu-west-1'
AWS_SES_REGION_ENDPOINT = 'email.eu-west-1.amazonaws.com'
DEFAULT_FROM_EMAIL = 'Snoweb <hello@snoweb.fr>'
EMAIL_USE_SSL = True
AWS_S3_OBJECT_PARAMETERS = {
    'CacheControl': 'public, max-age=31536000',
}
AWS_IS_GZIPPED = True
AWS_STORAGE_BUCKET_NAME = BUCKET_NAME
AWS_DEFAULT_ACL = 'public-read'
AWS_LOCATION = 'www/'
FOLDER_FILE_UPLOAD_S3 = 'www'
URL_BUCKET_FILE = 'https://s3-eu-west-3.amazonaws.com/' + AWS_STORAGE_BUCKET_NAME + '/' + FOLDER_FILE_UPLOAD_S3
S3DIRECT_REGION = 'eu-west-3'
AWS_S3_FILE_OVERWRITE = False

# Wagtail

WAGTAIL_SITE_NAME = SITE_NAME
WAGTAILDOCS_SERVE_METHOD = 'direct'
WAGTAIL_BLOG_AUTHOR_PAGE = 'account.User'
WAGTAIL_BLOG_POSTS_PER_PAGE = 25
RICH_TEXT_FEATURES = base_settings.RICH_TEXT_FEATURES
WAGTAILDOCS_DOCUMENT_MODEL = 'cms.MyDocument'

#  Bakery

BUILD_DIR = os.path.join(BASE_DIR, 'cms/templates/build')
BAKERY_VIEWS = (
    'webspace.bakery.views.wagtail.AllBuildablePagesView',
    'webspace.bakery.views.wagtail.BlogIndexTagPagesView',
    'webspace.bakery.views.wagtail.PortfolioIndexTagPagesView',
)
BAKERY_GZIP = True


#  Content Security Policy

CSP_DEFAULT_SRC = (
    "'self'",
    "releases.wagtail.io",
)
CSP_MANIFEST_SRC = (
    "'self'",
    'data:',
)
CSP_STYLE_SRC = (
    "'self'",
    'fonts.googleapis.com',
    "'unsafe-inline'",
)
CSP_SCRIPT_SRC = (
    "'self'",
    "cdn.ampproject.org",
    "www.google-analytics.com",
    "www.googletagmanager.com",
    "'unsafe-eval'",
    "'unsafe-inline'",
    "assets.calendly.com",
)

CSP_FONT_SRC = (
    "'self'",
    'fonts.googleapis.com',
    'fonts.gstatic.com',
    'data:',
    'blob:',
)
CSP_IMG_SRC = (
    "'self'",
    BUCKET_URL_CDN,
    'www.gravatar.com',
    "www.google-analytics.com",
    "www.googletagmanager.com",
    'data:',
)
CSP_FRAME_SRC = (
    "'self'",
    '*.vimeo.com',
    '*.youtube.com',
    'www.facebook.com',
    'assets.calendly.com',
    'calendly.com',
)

CSP_CONNECT_SRC = (
    "'self'",
    BUCKET_URL_CDN,
    "cdn.ampproject.org",
    "www.googletagmanager.com",
    "releases.wagtail.io",
    'fonts.googleapis.com',
    '*.vimeo.com',
    '*.youtube.com',
    'www.facebook.com',
    "www.google-analytics.com",
    'fonts.gstatic.com',
    "assets.calendly.com",
)

WY_LOCALE = 'en_US'
