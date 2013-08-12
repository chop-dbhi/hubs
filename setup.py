import sys
from setuptools import setup, find_packages


install_requires = [
    'django>=1.4,<1.6',
    'South>=0.8.2',
    'requests>=1.2,<1.3',
]

if sys.version_info < (2, 7):
    install_requires.append('argparse>=1.2.1')


kwargs = {
    'packages': find_packages(),

    'install_requires': install_requires,

    'test_suite': 'test_suite',

    'scripts': ['bin/hubs'],

    'name': 'hubs',
    'version': __import__('hubs').get_version(),
    'author': 'Byron Ruth',
    'author_email': 'b@devel.io',
    'description': 'Data hub management',
    'license': 'BSD',
    'keywords': 'data hub warehouse',
    'url': 'https://github.com/cbmi/hubs/',
    'classifiers': [
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Framework :: Django',
        'Topic :: Internet :: WWW/HTTP',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'Intended Audience :: Healthcare Industry',
        'Intended Audience :: Information Technology',
    ],
}

setup(**kwargs)
