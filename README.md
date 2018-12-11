# Final Project
Created By: Joanna Saikali  

## Set up:
The data is from the Kaggle location:
https://www.kaggle.com/luisfredgs/yelp-reviews-csv#yelp_review.csv

I used a function in pset_02/splitter.py to split that data into manageable chunks which you will find in `data/yelp/`

Be sure that the .gitignore contains the `data/` since the files are huge!

## Installations
- ./drun_app pipenv install dask
- ./drun_app pipenv install luigi

## Intro

In Problem Set 2, we performed word embeddings on our demographics survey. In Problem Set 3, we enhanced this work by incorporating Luigi into the workflow.

Now, we will be building off of Problem Set 2 to incorporate Dask Dataframes and Dask Delayed.

In this repo you will find working code of Problem Set 2. Starter code that should look like your own solution can be found in main.py.

Previously, in your problem set solution's `main.py`, you had something like this:
```
if __name__ == '__main__':
    # instantiate the embedding class
    embedding = WordEmbedding.from_files('data/words.txt', 'data/vectors.npy.gz')

    # read in the hashed student data
    data = load_data('data/hashed.xlsx')

    # create the vector representation for each survey entry
    vecs = data['learn'].apply(embedding.embed_document) \
           + data['project'].apply(embedding.embed_document)

    # transformed vector back into DataFrame with float types
    df = pandas.DataFrame([v for v in vecs.values], index=vecs.index)
```

But now we will be working with a Yelp Review dataset, so you will find this in the `main.py` file:
```
if __name__ == '__main__':
    # instantiate the embedding class
    embedding = WordEmbedding.from_files('data/words.txt', 'data/vectors.npy.gz')

    # read in the yelp review data
    data = pandas.concat([pandas.read_csv(f) for f in glob.glob('data/yelp/yelp_review_*.csv')], ignore_index = True)

    # subset the data for the vector portion - otherwise we have memory issues
    data_subset = data.sample(100000)

    # create the vector representation for each yelp review
    vecs = data_subset['text'].apply(embedding.embed_document)

    # transformed vector back into DataFrame with float types
    df = pandas.DataFrame([v for v in vecs.values], index=vecs.index)
```

## Problems (70 points)

## 1a. Dask Dataframe (5 pts)
Let's work with Dask dataframes instead of Pandas dataframes. Note that when you are asked to "output", it is expected that this is done through `main.py` with print statements

- In addition to the existing code reading dataframes as pandas, please read the csvs using `dask.dataframe`. Output the time elapsed for each case.
- In addition to sampling 100K rows of the pandas dataframe, do so for the dask dataframe. Output the time elapsed for each case.
- In addition to creating the vector representation for the pandas dataframe, do so for the dask dataframe, do so for the dask dataframe. Output the time elapsed for each case.
- After you transform the vector data back to a pandas dataframe, use dask's `from_pandas` method to convert it also into a dask dataframe called `df_dask`. We will be working with it later.

## 1b. embed_document
Change the `embed_document` method in the `WordEmbedding` class so that it leverages `dask.delayed`. Output the time elapsed when running `embed_document` on the dask dataframe with versus without `dask.delayed`.

## 2. Dask: Aggregating Metrics using Delayed and Dask Dataframes (40 pts)
Let's say we want a basic understanding of the characteristics of each star value, including the following
- Average text length
- Sum of "useful" votes
- Sum of "funny" votes
- Sum of "cool" votes
- Count of number of reviews

#### Traditional Way (5 pts)
Perform these aggregations the traditional way, using pandas dataframes & groupbys. Print the time elapsed to the console.

#### Dask Way (15pts)
Make a few changes:
- Leverage Dask Dataframes for those aggregations instead of Pandas
- Use Dask.Delayed for the calculations - this will allow each of the 5 stars to be processing in parallel

#### Dask Key-Value (10pts)
While it is not a good idea to change the index regularly just for calculations, you know that there are great benefits to it when you have a lot of computations that rely on grouping/filtering specific columns.

Given the aggregations you just did, what would the ideal Dask index be?

Run the aggregations again with said index, and report on the time it took for those aggregations.

#### Visualize (10pts)
Now, you know that Dask isn't ALL about speed. It is also about efficiency of running in parallel and distributing across your local machine.

Leverage ".visualize()" and print it to the console, to see the parallel processes going on for the aggregation done above.

## Word Vectors (25pts)
You now have these beautiful word vectors. I want to know - for each review, find the 5 closest neighbors, and report on:
- Average number of stars for those 5 neighbors
- Average text length

#### Find Distances (15pts)
We have a `find_distance` function in `pset_02/similarity_distance_functions.py` that was catered to our demographic survey results. Below is a similar function `find_distance_yelp` that, for the word vector at a given row index, should calculate distances to the vectors in other rows. It returns the distance vector with 100K rows, and the value at the index itself should be None.

Please Dask-ify it (use dask dataframes and dask.delayed), and run it in `main.py` iterating through the created yelp vector row-by-row:
```
def find_distance_yelp(vector_df, reference_index):

    # Extract the vector at the reference_index
    my_vec = vectors_df[vectors_df.index == reference_index].values[0]

    # Define a distance function
    def my_distance(vec):
        return 1 - cosine_similarity(vec, my_vec)

    distances = vectors_df.apply(my_distance, axis=1)

    distances[distances.index==reference_index]=None

    return distances
```

#### Calculate error (10 pts)
I am going to make a claim that "similar" reviews should have similar star value.

Create a function to calculate MSE, using the Dask dataframe and dask.delayed, which for two numbers A & B is calculated as follows:
```mse = ((A - B)**2).mean(axis=1)```

For reference, what would the MSE have been if we assigned random values 1-5 instead of finding neighbors?

### Feedback (10 points)

#### How many hours did this assignment take?  Too hard/easy/just right? (2 points)

#### What did you find interesting? Challenging? Tedious? (8 points)

## Python Quality (10 points)
Notes from TA may go here

## Git History (10 points)
Notes from TA may go here

## Total Grade
Notes from TA may go here
