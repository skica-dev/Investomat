try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'description': 'My Project',
    'author': 'Maksymilian Skica (m4k5)',
    'url': 'https://github.com/m4k5/',
    'download_url': 'https://github.com/m4k5',
    'author_email': 'maks@riseup.net',
    'version': '0.1',
    'install_requires': ['nose'],
    'packages': ['NAME'],
    'scripts': [],
    'name': 'projectname'
}

setup(**config)
