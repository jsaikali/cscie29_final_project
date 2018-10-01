"""
Created by: Joanna Saikali
Date: September 30, 2018
Purpose: Write similarity and distance functions for later use
"""

import numpy
import os
from pset_utils.hashing.hashing import hash_str

def cosine_similarity(a,b):
    return numpy.dot(a,b) / (numpy.linalg.norm(a) * numpy.linalg.norm(b))

def my_salt(github_username='jsaikali'):

    # Get the salt from the environment
    SALT = bytes.fromhex(os.environ['SALT'])

    # Get the first 8 digits of my hash
    my_hash = hash_str(github_username.lower(), salt=SALT).hex()[:8]

    return my_hash

