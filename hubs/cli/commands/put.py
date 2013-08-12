import os
import sys
from hubs.cli import logger
from hubs.cli.decorators import cli


@cli(description='Puts a URL, file, or string stream into the hub')
def parser(options):
    if options.quiet:
        logger.setLevel(logging.NOTSET)
    elif options.verbosity > 2:
        logger.setLevel(logging.DEBUG)
    elif options.verbosity > 1:
        logger.setLevel(logging.INFO)
    elif options.verbosity > 0:
        logger.setLevel(logging.WARNING)

    conf_path = os.path.join(options.root, 'hubconf.py')

    sys.path.insert(0, conf_path)
    os.environ['DJANGO_SETTINGS_MODULE'] = 'hubconf'

    from hubs.handlers import put

    async = not options.serial
    for source in options.source:
        put(source, async=async)


parser.add_argument('source', nargs='+', action='store',
    help='A URL, file path, or string stream')
parser.add_argument('-s', '--serial', action='store_true',
    help='By default, sources are handled in parallel. This forces them to be performed serially.')
parser.add_argument('-r', '--root', default=os.getcwd(), action='store', metavar='path',
    help='Path to the hub if not the current working directory.')
parser.add_argument('-v', '--verbose', action='count', dest='verbosity',
    help='Increases the verbosity of logging. Use multiple times to increase verbosity.')
parser.add_argument('-q', '--quiet', action='store_true',
    help='Turn off all logging')
