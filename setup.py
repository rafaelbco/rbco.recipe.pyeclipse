# -*- coding: utf-8 -*-
import os
from setuptools import setup, find_packages

def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()

version = '0.0.5'

long_description = (    
    read('rbco', 'recipe', 'pyeclipse', 'README.txt')
    + '\n' + read('CHANGES.txt')
    + '\n' + read('TODO.txt')
    + '\n' + read('CONTRIBUTORS.txt')    
)
entry_point = 'rbco.recipe.pyeclipse:Recipe'
entry_points = {"zc.buildout": ["default = %s" % entry_point]}

tests_require=['zope.testing', 'zc.buildout']

setup(name='rbco.recipe.pyeclipse',
      version=version,
      description="Creates a Pydev project for Eclipse.",
      long_description=long_description,
      # Get more strings from http://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        'Framework :: Buildout',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        ],
      keywords='eclipse pydev',
      author='Rafael Oliveira',
      author_email='rafaelbco@gmail.com',
      url='http://rbco-recipe-pyeclipse.googlecode.com/',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['rbco', 'rbco.recipe'],
      include_package_data=True,
      zip_safe=False,
      install_requires=['setuptools',
                        'zc.buildout',
                        'BeautifulSoup>=3.0.7a,<=3.2',
                        ],
      tests_require=tests_require,
      extras_require=dict(tests=tests_require),
      test_suite = 'rbco.recipe.pyeclipse.tests.test_docs.test_suite',
      entry_points=entry_points,
      )
