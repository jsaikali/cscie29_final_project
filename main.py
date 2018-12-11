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

if __name__ == '__main__':
    # instantiate the embedding class
    embedding = WordEmbedding.from_files('data/words.txt', 'data/vectors.npy.gz')

    # read in the yelp review data
    data = pandas.read_csv('data/yelp_review_subset.csv.zip')
                     
    # create the vector representation for each yelp review
    vecs = data['text'].apply(embedding.embed_document) 

    # transformed vector back into DataFrame with float types
    df = pandas.DataFrame([v for v in vecs.values], index=vecs.index)

    print(df.columns[1:5])
    print(df.head())
    print(data.head())
