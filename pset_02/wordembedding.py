"""
Created by: Joanna Saikali
Date: September 30 2018
Purpose: Word embeddings class
"""

from pset_02.load_datasets import load_data, load_words, load_vectors
import numpy


class WordEmbedding(object):
    def __init__(self, words, vecs):

        self.words = words
        self.vecs = vecs
        self.vecs_n = vecs.shape[1]  # length of each vector, i.e. the n in the 2D matrix with shape (m, n)

    def __call__(self, word):
        """Embed a word

        :returns: vector, or None if the word is outside of the vocabulary
        :rtype: ndarray
        """
        try:
            word_index = self.words.index(word)
            word_vector = self.vecs[word_index]
        except ValueError:
            word_vector = None

        return word_vector

    @classmethod
    def from_files(cls, word_file, vec_file):
        """Instanciate an embedding from files

        Example::

            embedding = WordEmbedding.from_files('words.txt', 'vecs.npy.gz')

        :rtype: cls
        """
        return cls(load_words(word_file), load_vectors(vec_file))

    def __tokenize__(self, text):
        import re
        # Get all "words", including contractions
        # eg tokenize("Hello, I'm Scott") --> ['Hello', "I'm", "Scott"]
        return re.findall(r"\w[\w']+", text.lower())

    def embed_document(self, text):
        """Convert text to vector, by finding vectors for each word and combining

        :param str document: the document (one or more words) to get a vector
            representation for

        :return: vector representation of document
        :rtype: ndarray (1D)
        """
        import functools
        words_from_doc = self.__tokenize__(text)  # tokenize the words from the doc

        vecs_from_doc = [self.__call__(x) for x in words_from_doc if x is not None]  # get the vector for each word
        vecs_from_doc_valid = [x for x in vecs_from_doc if x is not None]  # remove the None types

        if (len(vecs_from_doc_valid) > 0): # if there is at least one word found, add the vectors
            vecs_sum = functools.reduce(lambda x, y: x + y, vecs_from_doc_valid)
        else:  # if no found words, create a vector of 0's
            vecs_sum = numpy.zeros(self.vecs_n)

        return vecs_sum
