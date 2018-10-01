# -*- coding: utf-8 -*-
from pkg_resources import get_distribution, DistributionNotFound
from pset_02.load_datasets import load_data, load_words, load_vectors
from pset_02.wordembedding import WordEmbedding

"""Top-level package for pset 02."""

__author__ = """Joanna Saikali"""
__email__ = 'joanna.saikali@gmail.com'
try:
    __version__ = get_distribution(__name__).version
except DistributionNotFound:
    #package is not installed
    from setuptools_scm import get_version
    import os
    __version__ = get_version(
        os.path.dirname(os.path.dirname(__file__))
    )
