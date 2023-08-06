# -*- coding: UTF-8 -*-
from setuptools import setup
from datetime import date


__author__ = "Michel Wortmann"
__copyright__ = "Copyright %s, " % date.today().year + __author__
__version__ = '0.1'
__email__ = "wortmann@pik-potsdam.de"
__license__ = "MIT"
__url__ = "https://github.com/mwort/zotero_word_items_to_collection"

requirements = [
    "pyzotero"
]

classifiers = [
    "Development Status :: 3 - Alpha",
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: MIT License",
    "Topic :: Office/Business :: Office Suites",
    "Topic :: Scientific/Engineering",
]

with open("readme.md", "r") as fp:
    long_description = fp.read()

setup(name="zotero_word_items_to_collection",
      version=__version__,
      author=__author__,
      author_email=__email__,
      url=__url__,
      py_modules=["zotero_word_items_to_collection"],
      install_requires=requirements,
      description="Create Zotero collections from Word files",
      long_description=long_description,
      license=__license__,
      classifiers=classifiers,
      python_requires=">=3.5",
      entry_points={
          'console_scripts':
            ['zotero_word_items_to_collection = zotero_word_items_to_collection:main']
        }
      )
