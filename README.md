# Final Project
Modified By: Joanna Saikali  

## Intro

In Problem Set 2, we performed word embeddings on our demographics survey. In Problem Set 3, we enhanced this work by incorporating Luigi into the workflow.

Now, we will be building off of Problem Set 2 to incorporate Dask Dataframes and Dask Delayed.

In this repo you will find working code of Problem Set 2. Starter code that should look like your own solution can be found in main.py.

Previously, in your problem set solution's `main.py`, you had sometihng like this:
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

But now we will be working with a Yelp Review dataset, so you will find something like this:
```
if __name__ == '__main__':
    # instantiate the embedding class
    embedding = WordEmbedding.from_files('data/words.txt', 'data/vectors.npy.gz')

    # read in the yelp review data
    data = pandas.read_csv('data/yelp_review_subset.csv.zip')
                     
    # create the vector representation for each yelp review
    vecs = data['text'].apply(embedding.embed_document) 

    # transformed vector back into DataFrame with float types
    df = pandas.DataFrame([v for v in vecs.values], index=vecs.index)
```

## Problems (70 points)

## Dask Dataframe (5 pts)
Let's work with Dask dataframes instead of Pandas dataframes.

Please modify the code in main.py to read our csv as a dask dataframe. Then after the vector representation is created, transform that vector back into a Dask dataframe rather than the pandas dataframe.

Provide print statements to the console, reporting how long each step takes with Dask vs. Pandas.

## Dask: Aggregating Metrics using Delayed and Dask Dataframes (40 pts)
Let's say we want a basic understanding of the characteristics of each star value, including the following
- Average text length
- Sum of "useful" votes
- Sum of "funny" votes
- Sum of "cool" votes

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
We have a `find_distance` function that was catered to our demographic survey results. Please write a function `find_distance_yelp` to cater it to this new dataset. Be sure to leverage `dask.delayed`.

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
