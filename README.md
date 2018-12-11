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

    # read in the hashed student data
    data = pandas.read_csv('data/yelp_review_subset.csv.zip')
                     
    # create the vector representation for each survey entry
    vecs = data['text'].apply(embedding.embed_document) 

    # transformed vector back into DataFrame with float types
    df = pandas.DataFrame([v for v in vecs.values], index=vecs.index)
```

## Problems (80 points)


### Feedback (10 points)

#### How many hours did this assignment take?  Too hard/easy/just right? (2 points)

#### What did you find interesting? Challenging? Tedious? (8 points)


## Python Quality (10 points)
Notes from TA may go here

## Git History (10 points)
Notes from TA may go here

## Total Grade
Notes from TA may go here
