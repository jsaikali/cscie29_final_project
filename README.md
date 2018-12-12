# Final Project
Created By: Joanna Saikali  

## Set up:
The data is from the Kaggle location:
https://www.kaggle.com/luisfredgs/yelp-reviews-csv#yelp_review.csv

I used a function in pset_02/splitter.py to split that data into manageable chunks which you will find in `data/yelp/`, but you do not need to touch it. The data is already provided in this repo (sorry github for putting 70 MB files on the repo)

Be sure that the .gitignore contains `data/` moving forward!

Clone this repo - it should look like your pset_02 solution, but just use this for convenience.

### Installations
Please perform the following installations
- ./drun_app pipenv install dask
- ./drun_app pipenv install luigi
- ./drun_app pipenv install graphviz

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
    data = pandas.concat([pandas.read_csv(f) for f in glob.glob('data/yelp/yelp_review_subset_*.csv')], ignore_index=True)

    # subset the data for the vector portion - otherwise we have memory issues
    data_subset = data.sample(10000)

    # create the vector representation for each yelp review
    vecs = data_subset['text'].apply(embedding.embed_document)

    # transformed vector back into DataFrame with float types
    df = pandas.DataFrame([v for v in vecs.values], index=vecs.index)

    # utilize atomic_write to export results to data/embedded.csv
    filename = "data/embedded.csv"
    with atomic_write(filename) as f:
        df.to_csv(f)
```

## Problems (55 points)

## 1. Same thing - but with Dask! (20 pts)

### 1a. Dask Dataframe (5 pts)
Let's work with Dask dataframes instead of Pandas dataframes. Note that when you are asked to "Output", it is expected that this is done through `main.py` with print statements

1. In addition to the existing code reading dataframes as pandas, please read the csvs in `data/yelp/` using `dask.dataframe`. Report:
    - Time elapsed loading the data using pandas
    - Time elapsed loading the data using dask dataframes
2. In addition to creating the vector representation `vecs` for the pandas dataframe, do so for the dask dataframe. Report:
    - Time elapsed running `embed_document` on the pandas dataframe
    - Time elapsed running `embed_document` on the dask dataframe

### 1b. Dask Delayed (5pts)
When running the `embed_document` function off of the dask dataframe, we can further make it efficient ny leveraging `dask.delayed`.

Add a line of code to your main function to run the `embed_document` on the dask dataframe using `dask.delayed`.  method in the `WordEmbedding` class so that it leverages `dask.delayed`. In part 2 of the last question, you reported some timestamps. Now report:
- Time elapsed using embed_document on the dask dataframe WITH dask.delayed.

Is there a significant difference in computation speed?

### 1c. Visualize (10pts)
Now, you know that Dask isn't ALL about speed. It is also about efficiency of running in parallel and distributing across your local machine.

Leverage ".visualize()" and write it out to a file `data/task_graph.png`, to see the parallel processes going on for the function done above. Please be sure to include it in your submission.

## 2. Aggregating Metrics using Delayed and Dask Dataframes (20 pts)
Let's say we want a basic understanding of the characteristics of each star value, including the following
- Sum of "useful" votes
- Sum of "funny" votes
- Sum of "cool" votes
- Count of number of reviews

### 2a. Traditional Way (5 pts)
Perform these aggregations the traditional way, using pandas dataframes & groupbys. Print the time elapsed to the console.

Note: Make sure to use the full dataframe, not the subsetted/sampled one! The dataframe subsets containing only 10000 rows are intended for the word embedding portion, as that is computationally expensive.

### 2b. Dask Way (5pts)
Do the same thing leveraging Dask. At a minimum you should use the Dask Dataframe, but if possible, try to incorporate dask.delayed as well in such a way that each of the 5 stars is aggregated in parallel.

### 2c. Dask Key-Value (10pts)
While it is not a good idea to change the index regularly just for calculations, you know that there can be great benefits to it when you have a lot of computations that rely on grouping/filtering specific columns. Changing the index can be costly upfront, but if you're doing many queries and aggregations, it can be worthwhile

Given the aggregations you just did, what would the ideal Dask index be?

Run the aggregations again with said index, and report on the time it took for those aggregations. Don't include the time it takes to actually change the index, as that is definitely a costly operation.

In this case, was the re-indexing worth it? Why / why not?

## 3. Word/Distance Vectors Vectors (25pts)
You now have these beautiful word vectors. I want to know - for each review, find the closest neighbor, and report on:
- Average number of stars for those 5 neighbors

### 3a. Find Distances (10pts)
We have a `find_distance` function in `pset_02/similarity_distance_functions.py` that was catered to our demographic survey results. Below is a similar function `find_distance_yelp` that, for the word vector at a given row index, should calculate distances to the vectors in other rows. It returns the index of the "most similar" word vector.

Please put this function in the `pset_02/similarity_distance_functions.py` and run this on the word vector Pandas dataframe in `main.py` iterating through the created yelp vector row-by-row. Make sure to subset the dataframe to approximately 1000 rows so that your kernel doesn't die during this expensive computation.

Report how long it takes.

```
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
```
### 3a. Find Distances Dask (15pts)

Please read the word vector in with dask.dataframe and Dask-ify the above function (use dask dataframes and dask.delayed).

You can similarly run it in `main.py` iterating through the created yelp vector row-by-row.

Report the time elapsed in both cases.

### 3c. Calculate error (10 pts)
I am going to make a claim that "similar" reviews should have similar star value.

Create a function to calculate MSE, using the Dask dataframe and dask.delayed, which for two numbers A & B is calculated as follows:
`mse = ((A - B)**2).mean(axis=1)`

Note that above you already have the index of the "most similar" vector. You now need to tie it back to the star values for the reference vector vs. similar vector in order to do this calculation.

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
