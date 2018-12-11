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

    # read in the hashed student data
    data = pandas.read_csv('data/yelp_review_subset.csv.zip')
                     
    # create the vector representation for each survey entry
    vecs = data['text'].apply(embedding.embed_document) 

    # transformed vector back into DataFrame with float types
    df = pandas.DataFrame([v for v in vecs.values], index=vecs.index)

    print(df.columns[1:5])
    '''
    # utilize atomic_write to export results to data/embedded.csv
    filename = "data/embedded.csv"
    with atomic_write(filename) as f:
        df.to_csv(f)

    # Obtaining the distance from each entry
    distances = find_distance(filename)

    # Finding the 5 students closest to me
    closest_5 = distances.sort_values(ascending=True)[:5]
    closest_5_df = data.merge(closest_5.to_frame(), left_index=True, right_index=True, how='inner')
    print('\n================================================================== \n')
    print('**The 5 individuals with responses closest to me are:** \n'.upper())
    print(closest_5_df)

    # Finding the 5 students furthest from me
    furthest_5 = distances.sort_values(ascending=False)[:5]
    furthest_5_df = data.merge(furthest_5.to_frame(), left_index=True, right_index=True, how='inner')
    print('\n================================================================== \n')
    print('**The 5 individuals with responses furthest from me are:** \n'.upper())
    print(furthest_5_df)

    # removing the file created
    # os.remove(filename)

'''
