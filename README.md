# Pset 2  
Modified By: Joanna Saikali  

Note: Original prompt preserved in PROMPT.md. This file contains the minimum necessary information to navigate my answers  

[![Build Status](https://travis-ci.com/csci-e-29/pset_2-jsaikali.svg?token=X6M5v2tzTUCBJ9zS8gst&branch=master)](https://travis-ci.com/csci-e-29/pset_2-jsaikali)

## Problems (80 points)

### Including pset_utils (15 points)

I chose to create an API token through the environment and to add my CI_USER_TOKEN to my .env file and on travis via https://travis-ci.com/csci-e-29/pset_2-jsaikali/settings. I also chose to do this in both my pset_utils repo and my cookicutter repo. While I realize that I may not need an API token for all cookiecutter projects, and that I subsequently will need to add the token to the individual projects I create, I would prefer to have that capability there for the future (helping "me 6 months from now" since I will likely forget how this setup worked)

#### Docker/pipenv prep

I updated this part in my Cookiecutter repo (the prompt explicitly asked for this), as well as my pset_utils repo, since this is a generally accepted convention.

#### Create a Github API token

This was completed as expressed under "Including pset_utils." To be able to run this yourself, you will also need to create a .env file with CI_USER_TOKEN=123.. and to add this token to the travis environment variables.

#### Install the utils!

This is complete and functional.

#### Including the utils tests

I added the required lines to setup.cfg.

I chose to update my .travis.yml to explicitly run the`pytest pset_utils` in a separate test stage. Despite that this is suboptimal, I personally prefer to record separately the test results of pset_utils. The following was added to .travis.yml::  
    
    - stage: utiltest
      script: ./drun_app pytest pset_utils


### Student Embeddings (40 points)

#### Loading the data (5 points)
This work was completed in `pset_02/load_datasets.py` and tested in `tests/test_load_datasets.py`

#### Embedding (20 points)

I chose to add the tokenize function as a private method in the WordEmbedding class, as this class was the only use case for such a function in this problem set. You can find all work for the WordEmbedding class in `pset_02/wordembedding.py` and the tests in `tests/test_wordembedding.py`

The implementation of word embedding for a document (the hashed student responses in this case) can be found in `main.py`. This result was written as instructed to `data/embedded.csv` in `main.py` as well.

#### Cosine similarity (5 points)

This function can be found in `pset_02/similarity_distance_functions.py` and its test cases can be found in `tests/test_similarity_distance_functions.py`

#### Find your friends (10 points)
I inserted SALT=123.. in my .env file and my travis settings once again. To run this yourself, you will need to do the same.

The functions to find the distance from my peers' responses can be found in `pset_02/similarity_distance_functions.py`. The functions were implemented in `main.py` to identify the 5 individuals closest and furthest from my response. You can refer to the travis output for the master branch, but for reference, here are the 5 hashes closest and furthest from mine:

Closest: 4cee0953, 4ed588f4, 23e5ebb7, 99379a48, 304f4014
Furthest: bc369f45, 322ac11f, dcd8a5b8, 4585e17d, 1a8b00bd 

(For the actual responses you can see the console output)

These results make a lot of sense to me - the answers far from me were short & always left one of the cells blank, while my responses were quite thorough. The responses closest to me seem to have a similar background of having worked with ML in their day jobs. They also appeared to use a lot of the same words / literature as me. Very cool stuff!

### Atomic (re)writes (15 points)

To install the package into my environment I ran `./drun_app pipenv install atomicwrites`

My code for the rewritten atomic write is in `pset_02/atomic_writes.py`. The associated test cases were copy and pasted directly from the pset_utils package test cases, into `tests/test_atomic_write.py`. I am not aware of how I could have run these tests without having recreated the testing file.

I made sure the tests worked via `./drun_app pytest`


### Feedback (10 points)

#### How many hours did this assignment take?  Too hard/easy/just right? (2 points)
This assignment took me 12+ hours. Part of the reason is because I had to patch up some mistakes in my pset_utils, and I did struggle with the setup again although it was MUCH more clear than the last problem set (thank you!). I did find it a good level of challenging though. It exposed me to concepts I actually am interested in, and I did learn a lot from my implementations.

#### What did you find interesting? Challenging? Tedious? (8 points)
Learning how to "embed" a variable into my environment was challenging/tedious for me - I know that it is relatively simple, but I tend to struggle with proper setup more than anything. Also, it was challenging (but fun) to make my own decisions about where to implement/write my functions for this problem set. I hope to get feedback/opinions about my choices.

I don't think we reviewed overriding methods, and while it is expected that students have prior knowledge, I felt unprepared for the Atomic rewrites question. It was a bit too challenging for me.

My favorite thing by far was the cosine similarity calculation. It was fun to implement, and it was also highly applicable to my projects / day job. Being able to embed a document and calculate distances so quickly was eye opening for me.


## Python Quality (10 points)
Notes from TA may go here

## Git History (10 points)
Notes from TA may go here

## Total Grade
Notes from TA may go here
