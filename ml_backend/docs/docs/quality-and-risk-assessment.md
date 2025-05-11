# MovRec App

This system integrates trained NLP models with a user-friendly GUI forming a highly attractive web application. In this document we analyze the **Quality & Risk Assessment**.

## Quality Assessment

### Performance Metrics

We have pre-computed similarties between all movies avaiable in the dataset. Its quality is one of the most important aspect of our application.

Model's accuracy is measured using the **genre-based** metrics listed below. It is important to recommend as many liked movies as possible. But the model should also recommend new genres from time to time.

1. **Precision**

- Indicates the proportion of genres in the recommended movies that match genres from movies the user has previously liked.
- Precision is lower when many recommended movies include genres outside the user’s preferences.

2. **Recall**

- measures how many of the user’s preferred genres are actually represented in the recommended movies.
- Recall is lower when some of the genres the user has liked are missing from the recommendations.

3. **F1-Score**

- Harmonic mean between Precision and Recall. It reflects the balance between how precisely and how completely the model captures the user's genre preferences.

> The value of each metric is influenced by the number of genres in the user's profile and the number of recommended movies. This is discussed further in the Scalability section.

### Robustness & Reliability

There are several edge cases in our system:

- If a user has only liked movies from a single genre and requests 100 recommendations, the model may yield high **recall** (since the genre is likely included) but low **precision** (many other genres may be present in the recommendations).
- Conversely, if the user has liked a diverse set of genres but asks for only one recommendation, **precision** may be high if the genre matches, but **recall** is low as most genres are not represented in the single result. Recall can only drop if user has too many favourite genres to be covered by too few recommended movies.

- Computing cosine similarity of plot summaries (for content-based recommendations) over large datasets can be computationally expensive and may introduce latency.

### Scalability

As mentioned, the **genre-based metrics vary depending on context**. Consider this scenario:

**User has liked 1000 random movies**. Then we want to recommend 10 movies based on favourite genres.

Example results:

```json
{
  "precision": 1.0,
  "recall": 0.53,
  "f1_score": 0.7
}
```

Precision is high because all the recommended movies align well with the user's preferred genres, meaning every recommendation was relevant.
Recall is lower because the recommendation set is small (e.g., only 10 movies), so it covers only a fraction of the genres or movies the user actually likes. As a result, many liked movies were not recommended.

Now consider if the user has **liked only 10 movies** but wants 100 movies to be recommended:

```json
{
  "precision": 0.73,
  "recall": 1.0,
  "f1_score": 0.85
}
```

In this case, **recall improves** because more of the user’s preferred genres are covered. However, **precision drops** due to the inclusion of genres that the user hasn’t shown interest in.

This tradeoff between **precision** and **recall** is natural in content-based recommendation systems and often desirable when trying to balance relevance and novelty.

## Risk Assessment

### Operational & Performance Risks

- High concurrency (e.g., many simultaneous requests) may lead to database locking or performance degradation.
- Larger amount of available and recommended movies can lead to slow response times if the similarity lookups aren’t cached or indexed.

### Cold-start problem

- Brand-new users with no movie history. It is wise to first like a satisfactory high amount of movies before asking for first recommendation.

### Bias

- If the training set overrepresents certain genres, the model remains heavily biased. This results in **overpersonalization**, which creates a _filter bubble_ where users only see the same kinds of movies.

### Concept drift

- Results from the bias and overpersonalization of the model. As tastes change over time, stale models will degrade.

### Privacy & Security Risks

- The current API implementation lacks strong user authentication and authorization mechanisms.

- Handling user ratings or watch-history in compliance with GDPR or other regulations
