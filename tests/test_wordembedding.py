"""
Created by: Joanna Saikali
Date: October 1 2018
Purpose: Tests for `WordEmbedding` class.
"""

"""
Ensuring that cosine_similarity function produces expected results,
based on a calculation done by statistics resources online.
"""

def test_consistency():
    import numpy
    from pset_02.wordembedding import WordEmbedding
    embedding = WordEmbedding.from_files('data/words.txt', 'data/vectors.npy.gz')
    one_valid_word = embedding.embed_document('hi djalkfj')
    one_word = embedding.embed_document('hi')
    assert numpy.array_equal(one_valid_word, one_word)


def test_no_valid_words():
    import numpy
    from pset_02.wordembedding import WordEmbedding
    embedding = WordEmbedding.from_files('data/words.txt', 'data/vectors.npy.gz')
    not_a_word = embedding.embed_document('stgrfefgfdsytr')
    assert numpy.array_equal(not_a_word, numpy.zeros(300))
