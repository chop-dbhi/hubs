import os

TESTS_DIR = os.path.dirname(__file__)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(TESTS_DIR, 'hub.db')
    }
}

SECRET_KEY = 'abc123'

TIMEZONE = 'America/New_York'

INSTALLED_APPS = (
    'hubs',
    'tests',
    'south',
)

HUB_ROOT = os.path.join(TESTS_DIR, 'hubroot')

LOGGING = {
    'version': 1,
    'handlers': {
        'null': {
            'level': 'DEBUG',
            'class': 'django.utils.log.NullHandler'
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler'
        }
    },
    'loggers': {
        'hubs': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': True
        }
    }
}
