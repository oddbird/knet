"""
Django settings for knet project.

For more information on this file, see
https://docs.djangoproject.com/en/dev/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/dev/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# set the mode for this instance
valid_modes = {'dev', 'prod'}
MODE = str(os.environ.get('KNET_MODE', 'dev'))
if MODE not in valid_modes:
    raise ValueError("KNET_MODE must be one of %s" % valid_modes)


# utility for getting settings from the environment
NOT_PROVIDED = object()
def env(key, coerce=str, default=NOT_PROVIDED):
    try:
        default = default.get(MODE, NOT_PROVIDED)
    except AttributeError:
        pass

    if default is NOT_PROVIDED:
        val = os.environ.get(key)
        if val is None:
            raise ValueError("Environment variable %s is required." % key)
    else:
        val = os.environ.get(key, default)
    return coerce(val)


# utility for parsing a database url
def parse_database_url(url):
    from urllib.parse import urlparse
    url_parts = urlparse(url)
    return {
        'NAME': url_parts.path[1:],
        'USER': url_parts.username,
        'PASSWORD': url_parts.password,
        'HOST': url_parts.hostname,
        'PORT': url_parts.port,
        'ENGINE' : {
            'postgres': 'django.db.backends.postgresql_psycopg2',
            'mysql': 'django.db.backends.mysql',
            'sqlite': 'django.db.backends.sqlite3',
        }[url_parts.scheme],
    }


# Deployment config

SECRET_KEY = env('KNET_SECRET_KEY', default={'dev': 'development-secret-key'})
DEBUG = env('KNET_DEBUG', bool, default={'dev': True, 'prod': False})
TEMPLATE_DEBUG = DEBUG

ALLOWED_HOSTS = env(
    'KNET_ALLOWED_HOSTS',
    lambda s: [b.strip() for b in s.split(',')],
    default={'dev': '*'},
    )

DATABASES = {
    'default': env(
        'DATABASE_URL',
        parse_database_url,
        default={
            'dev': 'postgres://%s@/knet' % env(
                'USER', default='knet'),
            },
        )
}


# Application definition

INSTALLED_APPS = [
    'django.contrib.sessions',
    'django.contrib.staticfiles',
    'django.contrib.auth',
    'django.contrib.admin',
    'django.contrib.contenttypes',
    'django.contrib.messages',
    'south',
    'djangosecure',
    'floppyforms',
    'widget_tweaks',
    'knet.accounts',
    'knet.landing',
]

AUTH_USER_MODEL = 'accounts.User'

MIDDLEWARE_CLASSES = [
    'django.middleware.gzip.GZipMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'knet.urls'

TEMPLATE_DIRS = os.path.join(BASE_DIR, 'templates')

WSGI_APPLICATION = 'knet.wsgi.application'

# Internationalization
# https://docs.djangoproject.com/en/dev/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/dev/howto/static-files/

STATIC_URL = env('KNET_STATIC_URL', default='/static/')
STATIC_ROOT = env(
    'KNET_STATIC_ROOT', default=os.path.join(BASE_DIR, 'collected-assets'))
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]

INSTALLED_APPS += ['pipeline']

PIPELINE_ENABLED = env(
    'KNET_PIPELINE_ENABLED', coerce=bool, default={'dev': False, 'prod': True})

STATICFILES_STORAGE = {
    'prod': 'pipeline.storage.PipelineCachedStorage',
    'dev': 'pipeline.storage.PipelineStorage',
    }[MODE]

PIPELINE_CSS_COMPRESSOR = 'knet.assets.css.RCSSMinCompressor'
PIPELINE_JS_COMPRESSOR = 'pipeline.compressors.slimit.SlimItCompressor'

PIPELINE_CSS = {
    'screen': {
        'source_filenames': [
            'css/screen.css',
            ],
        'output_filename': 'css/screen.min.css',
        },
    'landing': {
        'source_filenames': [
            'css/landing.css',
            ],
        'output_filename': 'css/landing.min.css',
        },
    'demo': {
        'source_filenames': [
            'css/demo.css',
            ],
        'output_filename': 'css/demo.min.css',
        },
    }

PIPELINE_JS = {
    'main': {
        'source_filenames': [
            'js/base.js',
            'js/landing.js',
            'js/demo.js',
            'js/init.js',
            ],
        'output_filename': 'js/main.min.js',
        },
    'modernizr': {
        'source_filenames': [
            'js/plugins/modernizr.custom.02470.js',
            'js/plugins/modernizr.selectors.js',
            'js/plugins/elem-details.js',
            ],
        'output_filename': 'js/modernizr.min.js',
        },
    'plugins': {
        'source_filenames': [
            'js/libs/jquery.js',
            'js/libs/handlebars.runtime.js',
            'js/plugins/jquery.ba-dotimeout.js',
            'js/plugins/jquery.stopwatch.js',
            'js/plugins/jquery.form.js',
            'messages_ui/jquery.messages-ui.js',
            'messages_ui/message.js',
            ],
        'output_filename': 'js/plugins.min.js',
        },
    }

# Pipeline doesn't need to wrap JS in an anonymous function for us
PIPELINE_DISABLE_WRAPPER = True

INSTALLED_APPS += ['messages_ui']
MIDDLEWARE_CLASSES.insert(
    MIDDLEWARE_CLASSES.index(
        'django.contrib.messages.middleware.MessageMiddleware'
        ) + 1,
    'messages_ui.middleware.AjaxMessagesMiddleware',
    )


LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'handlers': {
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
        },
        'null': {
            'class': 'django.utils.log.NullHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
        },
        'django.request': {
            'handlers': ['console'],
            'level': 'ERROR',
            'propagate': False,
        },
        'py.warnings': {
            'handlers': ['console'],
        },
    }
}
