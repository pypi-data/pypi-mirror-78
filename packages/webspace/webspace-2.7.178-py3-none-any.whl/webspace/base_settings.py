import os
import json
import string
import random


def generate_secret_key(size=247, chars=string.ascii_letters + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def get_package_version(file_path):
    with open(file_path) as package:
        data = json.load(package)
        return data['version']


def run_sentry():
    import sentry_sdk
    from sentry_sdk.integrations.django import DjangoIntegration
    from sentry_sdk.integrations.logging import LoggingIntegration
    import logging
    sentry_sdk.init(
        dsn="https://677252655469434897723bab86b18ef0@o419846.ingest.sentry.io/5336964",
        integrations=[
            DjangoIntegration(),
            LoggingIntegration(
                level=logging.INFO,
                event_level=logging.ERROR
            )
        ],
        send_default_pii=True
    )


ALLOWED_HOSTS_DEV = [
    '127.0.0.1',
    'localhost',
    'home'
]

INSTALLED_APPS = [
    'webspace.account',
    'webspace.bakery.apps.BakeryConfig',

    'wagtail.contrib.forms',
    'wagtail.contrib.redirects',
    'wagtail.embeds',
    'wagtail.sites',
    'wagtail.users',
    'wagtail.snippets',
    'wagtail.documents',
    'wagtail.images',
    'wagtail.search',
    'wagtail.admin',
    'wagtail.core',
    'wagtail.contrib.settings',
    'wagtail.contrib.frontend_cache',

    'storages',
    'modelcluster',
    'taggit',
    'django_social_share',
    'wagtail_feeds',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    "django.contrib.sitemaps",

    'django_user_agents',
    'rosetta',

]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django_user_agents.middleware.UserAgentMiddleware',
    'django.middleware.gzip.GZipMiddleware',
    'webspace.middleware.ConfigMiddleware',
    'wagtail.contrib.redirects.middleware.RedirectMiddleware',
    'csp.middleware.CSPMiddleware',
]


def get_templates(base_dir):
    return [
        {
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'DIRS': [os.path.join(base_dir, 'templates')],
            'OPTIONS': {
                'context_processors': [
                    'django.template.context_processors.debug',
                    'django.template.context_processors.request',
                    'django.contrib.auth.context_processors.auth',
                    'django.contrib.messages.context_processors.messages',
                    'wagtail.contrib.settings.context_processors.settings',
                    'webspace.cms.amp.context_processors.amp'
                ],
                'loaders': [
                    'django.template.loaders.filesystem.Loader',
                    'django.template.loaders.app_directories.Loader',
                ],
                'libraries': {
                    'my': 'webspace.cms.templatetags.my',
                    'my_minify': 'webspace.cms.templatetags.my_minify',
                    'my_amp': 'webspace.cms.templatetags.my_amp',
                }
            },
        },
    ]


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

STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
]

RICH_TEXT_FEATURES = [
    'h1',
    'h2',
    'h3',
    'h4',
    'bold',
    'italic',
    'link',
    'ol',
    'ul',
    'hr',
    'code-block',
    'blockquote',
    'strikethrough',
    'mark',
    'shadow'
]

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            '()': 'webspace.formatter.DjangoColorsFormatter',
            'format': '[%(asctime)s] %(levelname)s\033[0m \033[1m%(name)s\033[0m (%(module)s.%(funcName)s.L%(lineno)d) -> %(message)s'
        },
        'success': {
            '()': 'webspace.formatter.DjangoColorsFormatter',
            'format': '\033[92m[%(asctime)s] SUCCESS\033[0m \033[1m%(name)s\033[0m (%(module)s.%(funcName)s.L%(lineno)d) -> %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        'null': {
            'level': 'DEBUG',
            'class': 'logging.NullHandler',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        },
        'success': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'success'
        },
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'propagate': True,
            'level': 'INFO',
        },
        'django.db.backends': {
            'handlers': ['null'],
            'propagate': False,
            'level': 'DEBUG',
        },
        'aws': {
            'handlers': ['console'],
            'propagate': True,
            'level': 'DEBUG',
        },
        'cms': {
            'handlers': ['success'],
            'propagate': True,
            'level': 'DEBUG',
        },
        'email': {
            'level': 'DEBUG',
            'propagate': True,
            'handlers': ['console'],
        },
        'bakery': {
            'level': 'DEBUG',
            'propagate': True,
            'handlers': ['console'],
        },
        'amp': {
            'level': 'DEBUG',
            'propagate': True,
            'handlers': ['console'],
        },
        'api': {
            'level': 'DEBUG',
            'propagate': True,
            'handlers': ['console'],
        },
        'celery': {
            'level': 'DEBUG',
            'propagate': True,
            'handlers': ['console'],
        },
        'minify_schema': {
            'level': 'DEBUG',
            'propagate': True,
            'handlers': ['console'],
        },
    }
}
