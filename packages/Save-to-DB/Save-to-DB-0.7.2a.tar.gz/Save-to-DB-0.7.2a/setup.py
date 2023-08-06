from distutils.core import setup

import os
import sys
import save_to_db
print(save_to_db.__file__)
sys.path.insert(0, os.path.dirname(save_to_db.__file__))


packages = []
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
def add_packages(path):
    global packages
    
    package_load_path = path.replace('/', '.').replace('\\', '.')
    packages.append(package_load_path)
    
    full_path = os.path.join(BASE_DIR, path)
    for filename in os.listdir(full_path):
        
        full_subpath = os.path.join(full_path, filename)
        if not os.path.isdir(full_subpath) or \
                not os.path.isfile(os.path.join(full_subpath, '__init__.py')):
            continue
        
        add_packages(os.path.join(path, filename))
        
add_packages('save_to_db')
packages.sort()


def readme():
    with open('README.rst') as fp:
        return fp.read()

DESCRIPTION = ('This library makes it easy to store data from any source '
               'into a database.')

setup(
    name = 'Save-to-DB',
    packages = packages,
    version = '0.7.2a',
    description = DESCRIPTION,
    long_description = readme(),
    author = 'Mikhail Aleksandrovich Makovenko',
    author_email = 'mma86@rambler.ru',
    url = 'https://bitbucket.org/mikhail-makovenko/save-to-db',
    download_url = \
        'https://bitbucket.org/mikhail-makovenko/save-to-db/get/0.7.2a.tar.gz',
    keywords = 'development scraping mining database',
    license = 'MIT',
    classifiers = [
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
    ],
)
