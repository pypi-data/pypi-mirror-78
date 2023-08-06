#!/usr/bin/env python
try:
    from setuptools import setup
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup

import xmltodict

with open('README.md') as f:
    long_description = f.read()


setup(name='gongtestfirst',
      version='1.2.2',
      long_description=long_description,
      long_description_content_type='text/markdown',
      author='gong',
      author_email='2976560783@qq.com',
      url='https://gitee.com/gongzhengyang',
      license='Apache License',
      platforms=['all'],
      python_requires='>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*',
      classifiers=[
          'Intended Audience :: Developers',
          'License :: OSI Approved :: MIT License',
          'Operating System :: OS Independent',
          'Programming Language :: Python',
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.4',
          'Programming Language :: Python :: 3.5',
          'Programming Language :: Python :: 3.6',
          'Programming Language :: Python :: 3.7',
          'Programming Language :: Python :: 3.8',
          'Programming Language :: Python :: Implementation :: Jython',
          'Programming Language :: Python :: Implementation :: PyPy',
          'Topic :: Text Processing :: Markup :: XML',
      ],
      py_modules=['gongtestfirst'],
      tests_require=['nose>=1.0', 'coverage'],
      )
