#!/usr/bin/env python

from distutils.core import setup

ldesc = '''
This module makes it easy to display animated or colored text on a
Pygame surface.  The name, pmtext, stands for Paper Mario Text.  Paper
Mario was my main inspiration in creating this module.

It works on my machine, even with unicode text.  But I haven't tested
it on other machines, so I'm setting the development status to Beta.
'''

setup(name='pmtext',
      version='0.1',
      description='Fancy Text for Pygame',
      long_description=ldesc,
      author='Charlie Murphy',
      author_email='cmsmurp00@gmail.com',
      packages=['pmtext'],
      classifiers=[
          'Development Status :: 4 - Beta',
          'Intended Audience :: Developers',
          'License :: Public Domain',
          'Programming Language :: Python :: 2'
          'Programming Language :: Python',
          'Topic :: Software Development :: Libraries :: pygame'
      ])
