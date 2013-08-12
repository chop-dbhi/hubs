import os
import sys
from hubs.cli import logger
from hubs.cli.decorators import cli


BLOCK_TEMPLATE = """\
{id}: {name}
source:\t{source}
date:\t{created}
"""

TABULAR_TEMLATE = '{id}\t{name}\t{source}\t{created}'


@cli(description='Lists all the files in the hub')
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

    from hubs.models import Stream

    if not Stream.objects.exists():
        print 'Nothing in the hub.'
        return

    template = options.tabular and TABULAR_TEMLATE or BLOCK_TEMPLATE

    for stream in Stream.objects.iterator():
        print template.format(**{
            'id': stream.pk,
            'name': stream.name,
            'source': stream.source,
            'created': stream.created
        })


parser.add_argument('-t', '--tabular', action='store_true',
    help='Shows a tabular output of list')
parser.add_argument('-r', '--root', default=os.getcwd(), action='store', metavar='path',
    help='Path to the hub if not the current working directory.')
parser.add_argument('-v', '--verbose', action='count', dest='verbosity',
    help='Increases the verbosity of logging. Use multiple times to increase verbosity.')
parser.add_argument('-q', '--quiet', action='store_true',
    help='Turn off all logging')
