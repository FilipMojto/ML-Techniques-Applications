from typing import List

import pandas as pd
import numpy as np

from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer

def recommend_movies(movie_df: pd.DataFrame,  user_liked_movies: List[str], matrix, count: int = 10):
    # Randomly select n movies from the entire dataset
    user_liked_movies = movie_df.sample(n=len(user_liked_movies), random_state=42)['title'].tolist()
    user_liked_movies = pd.Series(user_liked_movies)

    # Get all movie vectors for movies the user liked
    liked_movie_indices = movie_df[movie_df['title'].isin(user_liked_movies)].index
    # we get the subset of the entire tfidf matrix based on user liked movies
    liked_movie_vectors = matrix[liked_movie_indices]

    # mean is calculated of all movies user has interacted with
    # the result needs to be converted into 2D array with one row (1 x N)
    user_profile_vector = np.asarray(liked_movie_vectors.mean(axis=0)).reshape(1, -1)

    user_similarities = cosine_similarity(user_profile_vector, matrix).flatten()

    # Create DataFrame of movies with similarity scores
    movie_scores = pd.DataFrame({'title': movie_df['title'], 'similarity': user_similarities})

    # Filter out movies the user has already interacted with
    movie_scores = movie_scores[~movie_scores['title'].isin(user_liked_movies)]

    # Return top recommendations after filtering
    return movie_scores.sort_values(by='similarity', ascending=False).head(count)

def get_movie_texts(movie_df: pd.DataFrame, movie_titles):
    """Retrieve processed_text for given movie titles."""
    return movie_df[movie_df['title'].isin(movie_titles)]['processed_text'].tolist()

def test_accuracy(movie_df: pd.DataFrame, recommended_movies: pd.DataFrame, user_liked_movies: List[str], vectorizer: TfidfVectorizer | CountVectorizer):
    recommended_movies_list = list(recommended_movies['title'])
    # Get genres
    user_genres = get_movie_genres(movie_df=movie_df, movie_titles=user_liked_movies)
    recommended_genres = get_movie_genres(movie_df=movie_df, movie_titles=recommended_movies_list)

    # Calculate genre overlap
    TP_genre = len(user_genres & recommended_genres)  # Common genres
    FP_genre = len(recommended_genres - user_genres)  # Mismatched genres
    FN_genre = len(user_genres - recommended_genres)  # Missed genres

    # Calculate precision, recall, and F1-score based on genres
    precision_genre = TP_genre / (TP_genre + FP_genre) if (TP_genre + FP_genre) > 0 else 0
    recall_genre = TP_genre / (TP_genre + FN_genre) if (TP_genre + FN_genre) > 0 else 0
    f1_genre = (2 * precision_genre * recall_genre) / (precision_genre + recall_genre) if (precision_genre + recall_genre) > 0 else 0

    #Get processed_text of movies
    user_texts = get_movie_texts(movie_df=movie_df, movie_titles=user_liked_movies)
    recommended_texts = get_movie_texts(movie_df=movie_df, movie_titles=recommended_movies_list)

    # TF-IDF vectorization
    # vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = vectorizer.fit_transform(user_texts + recommended_texts)

    # Compute cosine similarity between liked & recommended movies
    user_vectors = tfidf_matrix[:len(user_texts)]
    recommended_vectors = tfidf_matrix[len(user_texts):]

    similarity_matrix = cosine_similarity(user_vectors, recommended_vectors)
    avg_similarity = np.mean(similarity_matrix)  # Average similarity across all pairs

    return {
        "precision": f"{precision_genre:.4f}",
        "recall": f"{recall_genre:.4f}",
        "f1_score": f"{f1_genre:.4f}",
        "text_similarity_score": f"{avg_similarity:.4f}"
    }    

def get_movie_genres(movie_df: pd.DataFrame, movie_titles):
    genres = movie_df[movie_df['title'].isin(movie_titles)]['genres']
    return set(genre.strip() for genre_list in genres.dropna() for genre in genre_list.split())