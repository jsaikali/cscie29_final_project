"""
Created by: Joanna Saikali
Date: September 30, 2018
Purpose: Prove my work to answer the embedding questions provided in PROMPT.md
Use: After building, you can run this via ./drun_app python main.py
"""

from pset_utils.io.io import atomic_write
from pset_02 import WordEmbedding, load_data, find_distance
import pandas
import os
import glob

if __name__ == '__main__':
    # instantiate the embedding class
    embedding = WordEmbedding.from_files('data/words.txt', 'data/vectors.npy.gz')

    # read in the yelp review data
    data = pandas.concat([pandas.read_csv(f) for f in glob.glob('data/yelp/yelp_review_*.csv')], ignore_index = True)

    # subset the data for the vector portion - otherwise we have memory issues
    data_subset = data.sample(100000)

    # create the vector representation for each yelp review
    vecs = data_subset['text'].apply(embedding.embed_document)

    # transformed vector back into DataFrame with float types
    df = pandas.DataFrame([v for v in vecs.values], index=vecs.index)
