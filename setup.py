from setuptools import setup, find_packages
import os


version = open('ftw/billboard/version.txt').read().strip()
maintainer = 'Julian Infanger'
tests_require = ['zope.testing',
                 'plone.app.testing',
                 'plone.mocktestcase',
                 ]

setup(name='ftw.billboard',
      version=version,
      description='Billboard for plone for publishing advertisements.',
      long_description=open('README.rst').read() + '\n' + \
          open(os.path.join('docs', 'HISTORY.txt')).read(),

      # Get more strings from
      # http://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        'Framework :: Plone',
        'Framework :: Plone :: 4.1',
        'Framework :: Zope2',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
        ],

      keywords='plone billboard ads advertisement ftw',
      author='4teamwork GmbH',
      author_email='mailto:info@4teamwork.ch',
      maintainer=maintainer,
      url='https://github.com/4teamwork/ftw.billboard',
      license='GPL2',

      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['ftw'],
      include_package_data=True,
      zip_safe=False,
      tests_require=tests_require,
      extras_require=dict(tests=tests_require),
      install_requires=[
        'plone.testing',
        'setuptools',
        # -*- Extra requirements: -*-
        ],

      entry_points='''
      # -*- Entry points: -*-
      [z3c.autoinclude.plugin]
      target = plone
      ''',
      )
