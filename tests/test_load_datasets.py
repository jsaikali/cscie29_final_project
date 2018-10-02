"""
Created by: Joanna Saikali
Date: September 30 2018
Purpose: Tests for `load_datasets` module.
"""


"""
Ensuring that load_data actually loads the desired file without errors,
and that it returns a pandas dataframe
"""
def test_load_data():
    import os
    import pandas
    from pset_02.load_datasets import load_data
    filename = 'data/hashed.xlsx'
    assert os.path.exists(filename)
    if os.path.exists(filename):
        data=load_data(filename)
    assert isinstance(data, pandas.DataFrame)

"""
Ensuring that load_vectors actually loads the desired file without errors,
and that it returns a numpy.ndarray
"""

def test_load_vectors():
    import os
    import numpy
    from pset_02.load_datasets import load_vectors
    filename = 'data/vectors.npy.gz'
    assert os.path.exists(filename)
    if os.path.exists(filename):
        vectors=load_vectors(filename)
    assert isinstance(vectors, numpy.ndarray)

"""
Ensuring that load_words actually loads the desired file without errors,
and that it returns a list
"""

def test_load_words():
    import os
    import numpy
    from pset_02.load_datasets import load_words
    filename = 'data/words.txt'
    assert os.path.exists(filename)
    if os.path.exists(filename):
        words=load_words(filename)
    assert isinstance(words, list)
