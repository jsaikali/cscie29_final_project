import pandas
import os
import numpy

def split(dataframe, row_limit=100000, output_name_template='yelp_review_%s.csv', output_path='data/yelp/', keep_headers=True):
    df_rows=dataframe.shape[0]
    num_partitions = numpy.ceil(df_rows/100000)
    for i in range(int(num_partitions)):
        dataframe_subset=dataframe[(i*row_limit):min((i+1)*row_limit,df_rows)]
        dataframe_subset.to_csv(os.path.join(
           output_path,
           output_name_template  % i),index=False)

data=pandas.read_csv('data/yelp_review.csv.zip')
split(data,output_path='data/yelp/')
