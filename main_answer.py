"""
Created by: Joanna Saikali
Date: September 30, 2018
Purpose: Prove my work to answer the embedding questions provided in PROMPT.md
Use: After building, you can run this via ./drun_app python main_answer.py
"""

from pset_utils.io.io import atomic_write
from pset_02 import WordEmbedding, load_data, find_distance
import pandas
import os
import time ##Q1
import glob ##Q1
import dask.dataframe as dd ##Q1
import csv ##Q1

if __name__ == '__main__':
    # instantiate the embedding class
    embedding = WordEmbedding.from_files('data/words.txt', 'data/vectors.npy.gz')
    print('started')
    # read in the yelp review data
    pd_start=time.time() ##Q1
    #data = pandas.read_csv('data/yelp_review.csv.zip')
    data = pandas.concat([pandas.read_csv(f) for f in glob.glob('data/yelp/yelp_review_*.csv')], ignore_index = True)
    print("pandas load took %f seconds" % (time.time()-pd_start)) ##Q1

    # read in the yelp review data using dask ##Q1
    dask_start=time.time() ##Q1
    data_dask = dd.read_csv('data/yelp/yelp_review_*.csv') #Q1
    print("dask load took %f seconds" % (time.time()-dask_start)) ##Q1

    # subset the data for the vector portion - otherwise we have memory issues
    pd_start=time.time() ##Q1
    data_subset = data.sample(100000)
    print("pandas subset took %f seconds" % (time.time()-pd_start)) ##Q1

    dask_start=time.time() ##Q1
    data_subset_dask = data_dask.sample(100000) ##Q1
    print("dask subset took %f seconds" % (time.time()-dask_start)) ##Q1

    # create the vector representation for each yelp review
    pd_start=time.time() ##Q1
    vecs = data_subset['text'].apply(embedding.embed_document)
    print("pandas vector took %f seconds" % (time.time()-pd_start)) ##Q1

    # create the vector representation for each yelp review
    dask_start=time.time() ##Q1
    vecs = data_subset_dask['text'].apply(embedding.embed_document)
    print("dask vector took %f seconds" % (time.time()-dask_start)) ##Q1

    # transformed vector back into DataFrame with float types
    df = pandas.DataFrame([v for v in vecs.values], index=vecs.index)
    df_dask = dd.from_pandas(df)

'''
import numpy

def calc_nchar_avg(series):
  nchars=[len(x) for x in series]
  return numpy.mean(nchars)

data.groupby('stars').agg({'useful': numpy.mean, 'funny': numpy.mean, 'cool': numpy.mean, 'review_id': 'count', 'text':calc_nchar_avg})

'''
#
# #from dask.delayed import delayed
# dfs = delayed(pandas.read_csv)('data/yelp_review.csv.zip')
#
# df = dd.from_delayed(dfs) # df is a dask dataframe''
#
# data2 = pandas.concat([pandas.read_csv(f) for f in glob.glob('data/yelp/yelp_review_4*.csv')], ignore_index = True)
#
# df = pd.read_csv(csvfile, header = None, delimiter="\t", quoting=csv.QUOTE_NONE, encoding='utf-8')