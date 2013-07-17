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


# utility for parsing a redis url
def parse_redis_url(url):
    from urllib.parse import urlparse
    url_parts = urlparse(url)


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

if MODE == 'prod':
    from redisify import redisify
    CACHES = redisify()
else:
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
            }
        }

STORY_CACHE_TIMEOUT = env('KNET_STORY_CACHE_TIMEOUT', int, default=1)

BASE_URL = env('KNET_BASE_URL', default={'dev': 'http://knet.hexxie.com:8000'})

SECURE_FRAME_DENY = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True

USE_SSL = env('KNET_USE_SSL', bool, default=False)

SESSION_COOKIE_SECURE = USE_SSL
SECURE_SSL_REDIRECT = USE_SSL
SECURE_HSTS_SECONDS = env('KNET_HSTS_SECONDS', int, default=0)
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
if USE_SSL:
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

ENABLE_LOGIN = env('KNET_ENABLE_LOGIN', bool, default=True)

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
    'form_utils',
    'widget_tweaks',
    'micawber.contrib.mcdjango',
    'knet',
    'knet.landing',
    'knet.accounts',
    'knet.teachers',
    ]

AUTH_USER_MODEL = 'accounts.User'

MIDDLEWARE_CLASSES = [
    'djangosecure.middleware.SecurityMiddleware',
    'django.middleware.gzip.GZipMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    ]

TEMPLATE_CONTEXT_PROCESSORS = [
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.tz',
    'django.core.context_processors.request',
    'django.contrib.messages.context_processors.messages',
    'knet.context_processors.settings',
    ]

TEMPLATE_LOADERS = [
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    ]

if MODE == 'prod':
    TEMPLATE_LOADERS = [
        ('django.template.loaders.cached.Loader', TEMPLATE_LOADERS)]

ROOT_URLCONF = 'knet.urls'

TEMPLATE_DIRS = os.path.join(BASE_DIR, 'templates')

WSGI_APPLICATION = 'knet.wsgi.application'

# Authentication

OAUTH_PROVIDER = env(
    'KNET_OAUTH_PROVIDER',
    default={
        'dev': 'oauth2.dummy.DummyOAuth',
        'prod': 'oauth2.facebook.FacebookOAuth',
        },
    )
OAUTH_CLIENT_ID = env('KNET_OAUTH_CLIENT_ID', default={'dev': ''})
OAUTH_CLIENT_SECRET = env('KNET_OAUTH_CLIENT_SECRET', default={'dev': ''})

LOGIN_REDIRECT_URL = 'login'

# Internationalization
# https://docs.djangoproject.com/en/dev/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'US/Eastern'

USE_I18N = True

USE_L10N = False

USE_TZ = True

DATE_INPUT_FORMATS = [
    '%m/%d/%Y',  # '10/25/2006'
    '%Y-%m-%d',  # '2006-10-25'
    '%m/%d/%y',  # '10/25/06'
    '%b %d %Y',  # 'Oct 25 2006'
    '%b %d, %Y', # 'Oct 25, 2006'
    '%d %b %Y',  # '25 Oct 2006'
    '%d %b, %Y', # '25 Oct, 2006'
    '%B %d %Y',  # 'October 25 2006'
    '%B %d, %Y', # 'October 25, 2006'
    '%d %B %Y',  # '25 October 2006'
    '%d %B, %Y', # '25 October, 2006'
]

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
    'modernizr': {
        'source_filenames': [
            'js/vendor/modernizr.custom.02470.js',
            'js/vendor/modernizr.selectors.js',
            'js/vendor/elem-details.js',
            ],
        'output_filename': 'js/modernizr.min.js',
        },
    'main': {
        'source_filenames': [
            'js/vendor/jquery.js',
            'js/vendor/handlebars.runtime.js',
            'js/vendor/jquery.ba-dotimeout.js',
            'js/vendor/jquery.form.js',
            'js/vendor/jquery.ajax-loading-overlay.js',
            'js/vendor/jquery.defuscate.js',
            'messages_ui/jquery.messages-ui.js',
            'messages_ui/message.js',
            'js/app/jstemplates.js',
            'js/app/base.js',
            'js/app/hbs_setup.js',
            'js/app/ajax_setup.js',
            'js/app/stories.js',
            'js/init.js',
            ],
        'output_filename': 'js/main.min.js',
        },
    'demo': {
        'source_filenames': [
            'js/vendor/jquery.stopwatch.js',
            'js/demo/demo.js',
            'js/demo/init.js'
            ],
        'output_filename': 'js/demo.min.js',
        }
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

GOOGLE_ANALYTICS_ID = env('KNET_GOOGLE_ANALYTICS_ID', default='')

if MODE == 'prod':
    INSTALLED_APPS += ['raven.contrib.django.raven_compat']
    RAVEN_CONFIG = {
        'dsn': env('SENTRY_DSN'),
        }
