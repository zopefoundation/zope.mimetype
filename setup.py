import os
from setuptools import setup, find_packages

def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()

name = "zope.mimetype"
setup(
    name = name,
    version = "1.0",
    author = "the Zope 3 project",
    author_email = "zope3-dev@zope.org",
    description = "A simple package for working with MIME content types",
    long_description=read('src', 'zope', 'mimetype', 'README.txt'),
    license = "ZPL 2.1",
    keywords = "MIME content type",
    url='http://svn.zope.org/zope.mimetype',

    packages = ['zope', 'zope.mimetype'],
    package_dir = {'': 'src'},
    namespace_packages = ['zope'],
    install_requires = ['setuptools'],
    include_package_data = True,
    )
