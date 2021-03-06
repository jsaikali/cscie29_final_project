"""
Created by: Joanna Saikali
Date: September 30, 2018
Purpose: Write similarity and distance functions for later use
"""

import numpy
import os
import pandas
from pset_utils.hashing.hashing import hash_str
import dask

"""
Compute a distance metric to represent how "similar" two words are
"""
def cosine_similarity(a,b):
    return numpy.dot(a,b) / (numpy.linalg.norm(a) * numpy.linalg.norm(b))


"""
Extract the first 8 digits of my response hash using the new salt which is in my .env file.
"""

def my_hash(github_username='jsaikali'):

    # Get the salt from the environment
    SALT = bytes.fromhex(os.environ['SALT'])

    # Get the first 8 digits of my hash
    my_hash = hash_str(github_username.lower(), salt=SALT).hex()[:8]

    return my_hash

"""
Compute the cosine distance between my response and every response in the class.
"""
def find_distance(vector_filename, github_username='jsaikali'):

    # Read in the vectors dataframe
    vectors_df = pandas.read_csv(vector_filename, index_col=0)

    # Get my hash
    hashed_username = my_hash(github_username)

    # Extract my personal vector
    my_vec = vectors_df[vectors_df.index == hashed_username].values[0]

    # Define a distance function
    def my_distance(vec):
        return 1 - cosine_similarity(vec, my_vec)

    distances = vectors_df[vectors_df.index != hashed_username].apply(my_distance, axis=1)

    # Dropping distance = 0, 1, Null
    # Corresponds to myself, prompt instructions, and blank entries
    distances = distances[((distances != 0) & (distances != 1) & (~distances.isnull()))]

    return distances

def find_distance_yelp(vector_df, my_vec):
    try:
        # Define a distance function
        def my_distance(vec):
            output = 1 - cosine_similarity(vec, my_vec)
            return output

        # Compute the distance vector for the row of reference
        distances = vector_df.apply(my_distance, axis=1)

        # Filter out the actual row itself (it's obviously closest to itself)
        distances = distances[distances.index!=my_vec.name]

        # Return the index of the word vector that is most similar
        return distances[distances==min(distances)].index[0]
    except:
        # Will reach this point if the word vector is all 0s, for example
        return

@dask.delayed
def find_distance_yelp_dask(vector_df, my_vec):
    try:
        # Define a distance function
        @dask.delayed
        def my_distance(vec):
            output = 1 - cosine_similarity(vec, my_vec)
            return output

        # Compute the distance vector for the row of reference
        distances = vector_df.apply(my_distance, axis=1)

        # Filter out the actual row itself (it's obviously closest to itself)
        distances = distances[distances.index!=my_vec.name]

        # Return the index of the word vector that is most similar
        return distances[distances==min(distances)].index[0]
    except:
        # Will reach this point if the word vector is all 0s, for example
        return
