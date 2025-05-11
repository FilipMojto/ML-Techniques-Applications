

# Quality Assessment

## Performance metrics

Model's accuracy is measured via following metrics:

1) **Precision**
- Is lower, if there have been movies recommended which user has not interacted with.
2) **Recall**
- Is lower, if there have been movies that user has interacted with but have not been recommended by the model.
3) **f1-score**
- Harmonic mean between first two metrics.

> The value of each metrics is dependent on the number of movies in user profile and on the number of recommended movies. This is more discussed in the Scalability section.

## Robustness & Reliability

There are several edge-cases possible in our system. For instance when user has only interacted with one movie but wants to recommend 100 movies or more. This usually results in perfect Recall (the movie is usually recommended) but very low Precision (many new movies recommended). 

In the opposite case, where user has a wide movie profile but wants only a single movie to be recommended there is a low probability of recommending new movie.

Computing the Cosine Similarity on the entire dataset for every request could be slow if the dataset is large.

## Scalability

We mentioned that the values of the metrics **vary depending on the context**. Consider the following example:

    User has interacted with 100 various movies. User asks system to recommend them 10 movies based on their personal profile.  

The results may look like this:

```json
{
  "precision": 0.7,
  "recall": 0.07,
  "f1_score": 0.1272727272727273,
  "recommendations": [
    {
      "title": "Bandits",
      "similarity": 0.21750030726751693
    },
    {
      "title": "The Dead Girl",
      "similarity": 0.21382390177095864
    },
    ...
  ]
}
```

Precision is quite high because model mainly recommends movies user has interacted with. This is because we recommend only the small portion (10) out of all movies in profile. Suppose however, user then asks model to recommend them 80 movies:

```json

{
  "precision": 0.475,
  "recall": 0.38,
  "f1_score": 0.4222222222222222,
  "recommendations": [
    {
      "title": "Bandits",
      "similarity": 0.21750030726751693
    },
    {
      "title": "The Dead Girl",
      "similarity": 0.21382390177095864
    },

    ...
  ]
}

```

We can observe from the results that Precision has dropped but the Recall has increased. Now the situation is different because with increased number of recommended movies model tends more to recommend movies user has interacted with but also the number of new (uninteracted) movies is higher.

From the perspective of a **content-based recommendation system** this is quite natural and desirable phenomenom.