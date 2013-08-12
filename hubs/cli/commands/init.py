import os
import sys
import logging
from hubs.cli import logger
from hubs.cli.decorators import cli


HUB_CONF_TEMPLATE = """\
import os

HUB_ROOT = os.path.dirname(__file__)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(HUB_ROOT, 'hub.db'),
    }
}

INSTALLED_APPS = (
    'hubs',
    'south',
)

SECRET_KEY = '%(secret_key)s'
"""

CHARSET = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'


@cli(description='Initializes a new hub')
def parser(options):
    path = options.path

    if options.stdout:
        print HUB_CONF
        sys.exit()

    if options.quiet:
        logger.setLevel(logging.NOTSET)
    elif options.verbosity > 2:
        logger.setLevel(logging.DEBUG)
    elif options.verbosity > 1:
        logger.setLevel(logging.INFO)
    elif options.verbosity > 0:
        logger.setLevel(logging.WARNING)

    # Ensure the path is kosher
    if not os.path.exists(path):
        os.makedirs(path)
        logger.info('Created directories for {0}'.format(path))
    elif not os.path.isdir(path):
        logger.error('{0} not a directory'.format(path))
        sys.exit(1)

    conf_path = os.path.join(path, 'hubconf.py')

    # Create the config if it doesn't already exist
    if os.path.exists(conf_path):
        logger.warning('Hub config already exists at {0}'.format(path))
    else:
        from django.utils.crypto import get_random_string
        secret_key = get_random_string(50, CHARSET)
        with open(conf_path, 'w') as conf:
            conf.write(HUB_CONF_TEMPLATE % {'secret_key': secret_key})
        logger.info('Created {0}'.format(conf_path))

    sys.path.insert(0, path)
    os.environ['DJANGO_SETTINGS_MODULE'] = 'hubconf'

    # Sync and migrate the database
    from django.core.management import call_command
    call_command('syncdb', migrate=True, interactive=False,
        verbosity=options.verbosity)
    logger.info('Hub database created')

    if not options.quiet:
        print 'Hub initialized at {0}'.format(path)


parser.add_argument('path', default=os.getcwd(), nargs='?',
    help='Path to the hub root.')
parser.add_argument('-s', '--stdout', action='store_true',
    help='Print the default configuration to standard out.')
parser.add_argument('-v', '--verbose', action='count', dest='verbosity', default=0,
    help='Increases the verbosity of logging. Use multiple times to increase verbosity.')
parser.add_argument('-q', '--quiet', action='store_true',
    help='Turn off all logging')
