"""
Created by: Joanna Saikali
Date: December 12, 2018
Purpose: Answer key for Final Project
Use: After building, you can run this via ./drun_app python main_answer.py
"""

from pset_utils.io.io import atomic_write
from pset_02 import WordEmbedding, load_data, find_distance
import pandas
import os
import time
import glob
import dask.dataframe as dd
import dask
import csv

if __name__ == '__main__':

    print("======== Question 1a & 1b & 1c Output ==========")
    # instantiate the embedding class
    embedding = WordEmbedding.from_files('data/words.txt', 'data/vectors.npy.gz')

    # read in the yelp review data
    pd_start=time.time()
    data = pandas.concat([pandas.read_csv(f) for f in glob.glob('data/yelp/yelp_review_subset_*.csv')], ignore_index=True)
    print("1a. pandas load took {} seconds".format(time.time()-pd_start)) ##Q1
    data=data.dropna()

    # read in the yelp review data using dask ##Q1
    dask_start=time.time()
    data_dask = dd.read_csv('data/yelp/yelp_review_subset_*.csv', encoding='utf-8', engine='python',
                            assume_missing=True, quoting=csv.QUOTE_NONE)  # Q1
    print("1a. dask load took {} seconds".format(time.time()-dask_start)) ##Q1
    data_dask=data_dask.dropna()

    # subset the data for the vector portion - otherwise we have memory issues
    pd_start=time.time()
    data_subset = data.sample(10000)

    # create the vector representation for each yelp review
    pd_start=time.time()
    vecs = data_subset['text'].apply(embedding.embed_document)
    print("1a. pandas vector took %f seconds" % (time.time()-pd_start)) ##Q1

    # create the vector representation for each yelp review using dask
    dask_start=time.time()
    vecs_dask = dd.from_pandas(data_subset,npartitions=10)['text'].apply(embedding.embed_document)
    print("1a. dask vector took %f seconds" % (time.time()-dask_start)) ##Q1

    # create the vector representation for each yelp review using dask AND dask delayed
    dask_start=time.time()
    vecs_dask_del = dd.from_pandas(data_subset,npartitions=10)['text'].apply(dask.delayed(embedding.embed_document))
    print("1b. dask vector WITH DELAYED took %f seconds" % (time.time()-dask_start)) ##Q1

    #vecs_dask_del.visualize(filename='data/task_graph.png')
    #print("1c. dask vector WITH DELAYED written out to {} seconds".format('data/task_graph.png')) ##Q1

    # transformed vector back into DataFrame with float types
    df = pandas.DataFrame([v for v in vecs.values], index=vecs.index)

    # utilize atomic_write to export results to data/embedded.csv
    filename = "data/embedded.csv"
    with atomic_write(filename) as f:
        df.to_csv(f)

    print("======== Question 2a Output ==========")
    import numpy

    metrics_start=time.time()
    metrics = data.groupby('stars').agg({'useful': numpy.mean, 'funny': numpy.mean, 'cool': numpy.mean, 'review_id': 'count'})
    print("2a. traditional metrics calculation took %f seconds. Metrics reported are:" % (time.time()-metrics_start))
    print(metrics)

    print("======== Question 2b Output ==========")

    metrics_start_dask=time.time()
    metrics_dask = data_dask.groupby('stars').agg({'useful': numpy.mean, 'funny': numpy.mean, 'cool': numpy.mean, 'review_id': 'count'})
    print("2b. dask df metrics calculation took %f seconds. Metrics reported are:" % (time.time()-metrics_start_dask))
    print(metrics_dask.compute())

    print("======== Question 2c Output ==========")

    def get_key(row):
        return '{}'.format(row.stars)

    ddf=data_dask.assign(
        key=data_dask[['stars']].apply(
            get_key, axis=1, meta=object)
    ).set_index('key')

    metrics_start_dask=time.time()
    metrics_dask = ddf.groupby('stars').agg({'useful': numpy.mean, 'funny': numpy.mean, 'cool': numpy.mean, 'review_id': 'count'})
    print("2c. dask df, new index, metrics calculation took %f seconds. Metrics reported are:" % (time.time()-metrics_start_dask))
    print(metrics_dask.compute())






