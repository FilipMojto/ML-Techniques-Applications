
Project background
===============

This document contains summarized project description including our motivation (buesin)

### Objective

Implement a supportive system will recommend the most suitable budget estimate for a particular movie.

### Dataset

Work with a public TMDB dataset available at

https://www.kaggle.com/datasets/tmdb/tmdb-movie-metadata

This dataset contains 5000 movies with their respective budgets with various other features.

### Steps

1) Business Understanding: Offer budget optimization for various stakeholders, like movie producers, studios, directors and many more.
2) Data Preprocessing: handling outliers, missing values, creating categories (< 1M, 1M<10M...), encoding categorical variables (genres, production companies...)
3) Modeling: Consider using Linear Regression, Random Forest... Split the data into training and testing datasets and validate the model's performance.

4) Evaluation: Experiment with various metrics

### Actions

- Define similarity measures (e.g. Pearson Colleration, cosine similarity, etc.)
- Experimenting with different data splitting ratios for training and testing.