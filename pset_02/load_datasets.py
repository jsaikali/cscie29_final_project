"""
Created by: Joanna Saikali
Date: September 30 2018
Purpose: Loading datasets for pset 02
"""


import numpy
import xlrd
import pandas


def load_words(filename):
    """Load a file containing a list of words as a python list

    :param str filename: path/name to file to load
    :rtype: list
    """

    with open(filename) as f:
        words = [word for line in f for word in line.split()]

    return words


def load_vectors(filename):
    """Loads a file containing word vectors to a python numpy array

    :param filename:

    :returns: 2D matrix with shape (m, n) where m is number of words in vocab
        and n is the dimension of the embedding

    :rtype: ndarray
    """
    array_file = open(filename, 'rb')
    array_obj = numpy.load(array_file)
    return array_obj


def load_data(filename, sheet_index=0, hashed_id_col='hashed_id', cols_to_drop=['']):
    """Load student response data

    :param str filename:

    :returns: dataframe indexed on a hashed github id
    :rtype: DataFrame
    """

    response_data = xlrd.open_workbook(filename)  # read excel workbook
    first_sheet = response_data.sheet_by_index(sheet_index)  # obtain the sheet desired

    # read the rows of data iteratively
    rows = []
    for i, row in enumerate(range(first_sheet.nrows)):
        r = []
        for j, col in enumerate(range(first_sheet.ncols)):
            r.append(first_sheet.cell_value(i, j))
        rows.append(r)

    # obtain the first row as header
    headers = rows.pop(0)
    df = pandas.DataFrame(rows, columns=headers)

    df = df.drop(cols_to_drop, axis=1)  # drop any columns (default to drop the undesirable index column)
    df = df.set_index(hashed_id_col)  # set the hashed_id column as the index
    df = df.fillna('')  # fill nas with blanks

    return df

