"""
Created by: Joanna Saikali
Date: September 30, 2018
Purpose: Write similarity and distance functions for later use
"""

import numpy
import os
#from pset_utils.hashing.hashing import hash_str

def cosine_similarity(a,b):
    return numpy.dot(a,b) / (numpy.linalg.norm(a) * numpy.linalg.norm(b))

def my_salt(github_username='jsaikali'):

    # Get the salt from the environment
    SALT = bytes.fromhex(os.environ['SALT'])

    # Get the first 8 digits of my hash
    my_hash = hash_str(github_username.lower(), salt=SALT).hex()[:8]

    return my_hash
def hash_str(some_val, salt=''):
    """Write a hash given

    :param some_val: str to be hashed
    :param salt: str or bytes string. Prefix that may be added to increase the randomness or otherwise change the outcome

    Example::

      hash_str('world!', salt='hello, ').hex()[:6] == '68e656'

    """
    import hashlib
    m = hashlib.sha256()  # instantiate the hash
    try:  # if salt is a string, add as prefix to the hash accordingly
        m.update(salt.encode('utf-8'))
    except Exception as e:  # if salt is byte, add as prefix to the hash accordingly
        m.update(salt)
    m.update(some_val.encode('utf-8'))  # add the string value
    return m.digest()  # return the digest

