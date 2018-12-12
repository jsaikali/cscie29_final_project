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
    #data = pandas.read_csv('data/yelp_review.csv.zip')
    data = pandas.concat([pandas.read_csv(f) for f in glob.glob('data/yelp/yelp_review_subset_*.csv')], ignore_index = True)

    # subset the data for the vector portion - otherwise we have memory issues
    data_subset = data.sample(10000)

    # create the vector representation for each yelp review
    vecs = data_subset['text'].apply(embedding.embed_document)

    # transformed vector back into DataFrame with float types
    df = pandas.DataFrame([v for v in vecs.values], index=vecs.index)

    # utilize atomic_write to export results to data/embedded.csv
    filename = "data/embedded.csv"
    with atomic_write(filename) as f:
        df.to_csv(f)
