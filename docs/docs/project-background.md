
Project background
===============

This document contains summarized project description including our motivation (buesin)

## Objective

Implement a content-based recommendation system that will recommend movies to user based on their personal profile.

## Dataset

Work with a public TMDB dataset available at

[TMDB Movie dataset](https://www.kaggle.com/datasets/tmdb/tmdb-movie-metadata)

This dataset contains 5000 movies with their respective budgets with various other features.

## Steps

1) Business Understanding: Focus on enhancing user experience by providing movie recommendations that closely match their interests and past interactions. Consider the impact of accurate content-based recommendations on user discovery and satisfaction. 

2) Data Preprocessing: Remove stop words, apply stemming or lemmatization, and vectorize the text using TF-IDF (Term Frequency-Inverse Document Frequency).

3) Modeling: Create user profiles based on their past interactions with movies and use cosine similarity to compare these profiles with movie vectors. Implement a system that ranks movies based on their similarity to the user profile.

4) Evaluation: Use precision, recall, and F1-score to evaluate the effectiveness of your recommender system. These metrics will help you understand both the accuracy and relevance of the recommended items.

## Actions

- Choose different techniques for text preprocessing (e.g., CountVectorizer vs. TF-IDF Vectorizer)
- Choice of similarity measures (e.g., cosine similarity, Euclidean distance) for comparing content and user profiles.