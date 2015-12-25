try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'description': 'Simple utility for geographical calculations',
    'author': 'Eriza Fazli',
    'url': 'https://github.com/herrfz/geoutils',
    'download_url': 'https://github.com/herrfz/geoutils',
    'author_email': 'erizzaaaaa@gmail.com',
    'version': '0.1',
    'install_requires': ['nose'],
    'packages': ['geoutils'],
    'scripts': [],
    'name': 'geoutils'
}

setup(**config)
