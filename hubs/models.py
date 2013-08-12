import os
import uuid
import logging
import mimetypes
from django.db import models
from django.utils import timezone
from django.conf import settings
from django.utils.text import slugify
from django.core.exceptions import ImproperlyConfigured
from utils import file_md5

HUB_ROOT = getattr(settings, 'HUB_ROOT', None)

if not HUB_ROOT:
    raise ImproperlyConfigured('The HUB_ROOT setting must be defined')

if not os.path.isabs(HUB_ROOT):
    raise ImproperlyConfigured('HUB_ROOT must be an absolute path')

logger = logging.getLogger('hubs')

# Initialize mimetypes once. TODO support explicit file to ensure
# compatibility?
mimetypes.init()


class Origin(models.Model):
    """The origin of data sources which could be a facility, institution,
    person, etc.
    """

    name = models.CharField(max_length=200, unique=True)
    path = models.CharField(max_length=200)

    @property
    def abspath(self):
        return os.path.abspath(os.path.join(HUB_ROOT, self.path))

    def save(self, *args, **kwargs):
        if not self.name:
            raise ValueError('name is required')

        if not self.pk and Origin.objects.filter(name=self.name).exists():
            raise ValueError('name must be unique')

        if not self.path:
            self.path = slugify(unicode(self.name))
            logger.info('Slugified origin name for path', extra={
                'origin': self.name,
                'path': self.path,
            })

        if not os.path.exists(self.path):
            os.makedirs(self.abspath)
            logger.info('Created origin directory in HUB_ROOT', extra={
                'origin': self.name,
                'path': self.abspath
            })
        return super(Origin, self).save(*args, **kwargs)


class Stream(models.Model):
    "A stream of data which can originate from a number of sources."

    name = models.CharField(max_length=200, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    origin = models.ForeignKey(Origin, null=True, blank=True)
    source = models.CharField(max_length=256, null=True, blank=True)
    stream = models.BooleanField(default=False)
    content_path = models.CharField(max_length=200, null=True, blank=True)
    content_type = models.CharField(max_length=50, null=True, blank=True)
    content_encoding = models.CharField(max_length=50, null=True, blank=True)
    md5 = models.CharField(max_length=40, null=True)
    size = models.IntegerField(null=True)
    started = models.DateTimeField(null=True)
    ended = models.DateTimeField(null=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta(object):
        ordering = ('-modified',)

    def __repr__(self):
        name = self.name or self.pk
        origin = self.origin_id and self.origin.name or 'Anonymous'
        return '<Stream "{0}" for "{1}">'.format(name, origin)

    def __iter__(self):
        return self.raw()

    def raw(self):
        if not self.content_path:
            return
        with open(self.content_path) as raw_stream:
            for chunk in raw_stream:
                yield chunk

    @property
    def content(self):
        return open(self.content_path, 'rb')

    def find_duplicates(self):
        "Returns a queryset containing duplicate streams based on the MD5."
        if not self.md5:
            return
        duplicates = Stream.objects.fiter(md5=self.md5)
        if self.pk:
            duplicates = duplicates.exclude(pk=self.pk)
        return duplicates

    def has_duplicates(self):
        "Returns a boolean if duplicates exist."
        duplicates = self.find_duplicates
        if duplicates is None:
            return
        return duplicates.exists()

    @property
    def abspath(self):
        "Returns the absolute path of the content path."
        if self.origin_id:
            parent = self.origin.path
        else:
            parent = 'anonymous'
        return os.path.join(HUB_ROOT, parent, self.content_path)

    def generate_path(self, name = None):
        """Prefixes a filename with a UUID for file storage.

        The output form is:

            16/fd2706-8baf-433b-82eb-8c7fada847da-<filename>

        The first two bytes will be a subdirectory and the remaining bytes
        will be prepended to the filename.
        """
        if not name:
            name = 'stream'
        else:
            name = '.'.join([ slugify(unicode(t)) for t in name.split('.') ])

        prefix = str(uuid.uuid4())
        subdir, prefix = (prefix[:2], prefix[2:])
        return os.path.join(subdir, '{0}-{1}'.format(prefix, name))

    def write(self, writer, source, binary = True, *args, **kwargs):
        "Takes a stream writer and writes the content."
        if self.content_path:
            if os.path.exists(self.content_path):
                raise ValueError('The stream content already exists')

        self.content_path = self.generate_path(self.name)
        os.makedirs(os.path.dirname(self.abspath))

        # TODO add exception handling
        self.started = timezone.now()
        with open(self.abspath, binary and 'wb' or 'w') as dest:
            writer(dest, source, *args, **kwargs)
        self.ended = timezone.now()

    def update_metadata(self, force = False):
        if self.content_path:
            mimetype, encoding = mimetypes.guess_type(self.content_path)

            if force or not self.content_type:
                self.content_type = mimetype
            if force or not self.content_encoding:
                self.content_encoding = encoding

        if force or self.size is None:
            self.size = os.path.getsize(self.abspath)
        if force or not self.md5:
            self.md5 = file_md5(self.abspath)

    def save(self, *args, **kwargs):
        if not self.pk:
            self.update_metadata()
        return super(Stream, self).save(*args, **kwargs)
