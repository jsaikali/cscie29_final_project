"""
Created by: Joanna Saikali
Date: September 30 2018
Purpose: Tests for `similarity_distance_functions` module.
"""

"""
Ensuring that cosine_similarity function produces expected results,
based on a calculation done by statistics resources online.
"""


def test_cosine_similarity():
    from pset_02.similarity_distance_functions import cosine_similarity
    assert round(cosine_similarity([1, 2, 4], [3, 5, 4]), 4) == 0.8950


"""
Ensuring that my hash returns the expectation of 33a0b58b
"""


def test_my_salt():
    from pset_02.similarity_distance_functions import my_salt
    assert my_salt() == '33a0b58b'
