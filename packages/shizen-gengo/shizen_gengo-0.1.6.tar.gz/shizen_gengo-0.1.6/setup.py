# -*- coding: utf-8 -*-

from distutils.core import setup
from setuptools import find_packages
from shizen_gengo import __version__

# read the contents of your README file
from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
  name = 'shizen_gengo',
  # packages = ['shizen_gengo'],
  packages=find_packages(exclude=('tests', 'docs')),
  version = __version__,
  license='	gpl-3.0',
  description = 'Python Library for common NLP Tasks',
  long_description=long_description,
  long_description_content_type='text/markdown',
  author = 'raoul biagioni',
  author_email = 'raoulbia.research@gmail.com',
  url = 'https://github.com/raoulbia/shizen_gengo.git',
  project_urls={
        "Documentation": "https://shizen-gengo.readthedocs.io/en/latest/"
    },
  # download_url = 'https://github.com/raoulbia/shizen_gengo/archive/0.1.0.tar.gz',
  keywords = ['nlp', 'pandas', 'dataframe'],
  install_requires=['nltk',
                  'pandas',
                  'numpy'
                  ],
  extras_require={'docs': ['commonmark',
                           'recommonmark',
                            'sphinx',
                            'sphinx_rtd_theme',
                            'sphinxcontrib.bibtex',
                            'sphinxcontrib.inlinesyntaxhighlight'],
                'tests': ['pytest']
                }

)

