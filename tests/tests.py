import os
import time
import shutil
import subprocess
from cStringIO import StringIO
from django.test import TestCase
from django.conf import settings
from django.http import HttpRequest
from django.core.files.base import ContentFile

import hubs
from hubs.utils import file_md5
from hubs.models import Origin, Stream


DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')


def pick(obj, keys):
    if hasattr(obj, '__dict__'):
        obj = obj.__dict__
    return dict([ (k, obj[k]) for k in obj if k in keys ])


class HubSetup(TestCase):
    def setUp(self):
        if os.path.exists(settings.HUB_ROOT):
            shutil.rmtree(settings.HUB_ROOT)


class OriginTestCase(HubSetup):
    def test(self):
        o = Origin(name='Test1')
        o.save()
        self.assertEqual(o.path, 'test1')
        self.assertTrue(os.path.exists(o.abspath))


class StreamTestCase(HubSetup):
    def test_default(self):
        source = 'Plain Text'

        s = hubs.put(source)

        data = {
            'name': None,
            'description': None,
            'size': 10,
            'content_type': None,
            'content_encoding': None,
            'stream': False,
            'source': None
        }

        self.assertEqual(pick(s, data.keys()), data)

    def test_path(self):
        source = os.path.join(DATA_DIR, 'users.csv')

        s = hubs.put(source)

        data = {
            'name': 'users.csv',
            'description': None,
            'size': 114,
            'content_type': 'text/csv',
            'content_encoding': None,
            'stream': False,
            'source': source,
            'content_path': source
        }

        self.assertEqual(pick(s, data.keys()), data)

    def test_path_copy(self):
        source = os.path.join(DATA_DIR, 'users.csv')

        s = hubs.put(source, copy=True)

        data = {
            'name': 'users.csv',
            'description': None,
            'size': 114,
            'content_type': 'text/csv',
            'content_encoding': None,
            'stream': False,
            'source': source
        }

        self.assertEqual(pick(s, data.keys()), data)

        # New path since it was a copy
        self.assertNotEqual(source, s.content_path)

        # Compare md5s
        self.assertEqual(file_md5(source), s.md5)

    def test_files_python(self):
        source = open(os.path.join(DATA_DIR, 'users.csv'), 'rb')

        s = hubs.put(source)

        data = {
            'description': None,
            'size': 114,
            'content_type': 'text/csv',
            'content_encoding': None,
            'stream': False,
            'source': source.name
        }

        self.assertEqual(pick(s, data.keys()), data)

    def test_files_django(self):
        source = ContentFile('Content File', name='upload.txt')

        s = hubs.put(source)

        data = {
            'description': None,
            'size': 12,
            'content_type': 'text/plain',
            'content_encoding': None,
            'stream': False,
            'source': 'upload.txt'
        }

        self.assertEqual(pick(s, data.keys()), data)

    def test_files_stringio(self):
        source = StringIO()
        source.write('String Buffer')
        source.seek(0)

        s = hubs.put(source)

        data = {
            'description': None,
            'size': 13,
            'content_type': None,
            'content_encoding': None,
            'stream': False,
            'source': None
        }

        self.assertEqual(pick(s, data.keys()), data)

    def test_http(self):
        source = 'http://localhost:8328/users.csv'

        # Start web server subprocess
        server = subprocess.Popen(['python', '-m', 'SimpleHTTPServer', '8328'],
            cwd=DATA_DIR, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        # Ensure server starts since the subprocess starts asynchronously
        time.sleep(1)

        s = hubs.put(source)

        # Kill the server
        server.terminate()

        data = {
            'name': 'users.csv',
            'description': None,
            'size': 114,
            'content_type': 'text/csv',
            'content_encoding': None,
            'stream': False,
            'source': source
        }

        self.assertEqual(pick(s, data.keys()), data)

        # Compare md5s
        self.assertEqual(file_md5(os.path.join(DATA_DIR, 'users.csv')), s.md5)

    def test_request(self):
        request = HttpRequest()

        request.META = {
            'REMOTE_ADDR': '127.0.0.1'
        }

        request.FILES = {
            'upload.txt': ContentFile('Content File', name='upload.txt')
        }

        s = hubs.put(request)

        data = {
            'name': 'upload.txt',
            'description': None,
            'size': 12,
            'content_type': 'text/plain',
            'content_encoding': None,
            'stream': False,
            'source': '127.0.0.1'
        }

        self.assertEqual(pick(s, data.keys()), data)
