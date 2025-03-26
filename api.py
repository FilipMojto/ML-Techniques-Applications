from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Literal
import pickle
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from scipy.sparse import spmatrix
import numpy as np
import sqlite3
from pathlib import Path
import os, sys


PROJECT_ROOT = Path(os.getcwd()).parent

# Add it to sys.path
sys.path.append(str(PROJECT_ROOT))

from ML_pipeline.isa_project_1.config import MODELS_DIR, PROCESSED_DATA_DIR
from ML_pipeline.testing import recommend_movies, test_accuracy

# Load the stored TF-IDF data
with open(MODELS_DIR / "tfidf_matrix.pkl", "rb") as f:
    tfidf_matrix: spmatrix = pickle.load(f)

with open(MODELS_DIR / "tfidf_vectorizer.pkl", "rb") as f:
    tfidf_vectorizer: TfidfVectorizer = pickle.load(f)

with open(MODELS_DIR / "count_matrix.pkl", "rb") as f:
    count_matrix: spmatrix = pickle.load(f)

with open(MODELS_DIR / "count_vectorizer.pkl", "rb") as f:
    count_vectorizer: CountVectorizer = pickle.load(f)

movie_df: pd.DataFrame = pd.read_pickle(PROCESSED_DATA_DIR / "movie_df.pkl")

# Initialize FastAPI app
app = FastAPI()

# Connect to SQLite database (or create it if it doesn't exist)
DATABASE_URL = "./data/example.db"

def get_db_connection():
    conn = sqlite3.connect(DATABASE_URL)
    conn.row_factory = sqlite3.Row
    return conn

# Create the database schema if it doesn't exist
def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY,
        username TEXT NOT NULL UNIQUE
    )''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS user_movie_list (
        user_id INTEGER,
        movie_title TEXT,
        FOREIGN KEY (user_id) REFERENCES users(user_id)
    )''')

    conn.commit()
    conn.close()

init_db()

# Pydantic models to define the structure of the input data
class RecommendRequest(BaseModel):
    username: str
    no_of_recommendations: int = 10
    method: Literal["tfidf", "count"] = "tfidf"  # Choice of similarity method

class MovieRecommendation(BaseModel):
    title: str
    similarity: float

class RecommendationResponse(BaseModel):
    precision: float
    recall: float
    f1_score: float
    recommendations: List[MovieRecommendation]

class UserProfile(BaseModel):
    username: str
    liked_movies: List[str]

# CRUD operations for managing user movie lists
@app.post("/user/", response_model=UserProfile)
async def create_user(user: UserProfile):
    """Create a new user and their movie list."""
    conn = get_db_connection()
    cursor = conn.cursor()

    # Create user in the users table
    try:
        cursor.execute("INSERT INTO users (username) VALUES (?)", (user.username,))
        user_id = cursor.lastrowid

        # Add user's liked movies to the user_movie_list table
        for movie in user.liked_movies:
            cursor.execute("INSERT INTO user_movie_list (user_id, movie_title) VALUES (?, ?)", (user_id, movie))

        conn.commit()
        conn.close()
    except sqlite3.IntegrityError:
        raise HTTPException(status_code=409, detail="User already exists")

    return user

@app.get("/user/{username}", response_model=UserProfile)
async def get_user_profile(username: str):
    """Get the user profile (movie list)."""
    conn = get_db_connection()
    cursor = conn.cursor()

    # Get user info
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    user = cursor.fetchone()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user_id = user["user_id"]

    # Get the user's movie list
    cursor.execute("SELECT movie_title FROM user_movie_list WHERE user_id = ?", (user_id,))
    liked_movies = [row["movie_title"] for row in cursor.fetchall()]

    conn.close()

    return UserProfile(username=username, liked_movies=liked_movies)

@app.put("/user/{username}", response_model=UserProfile)
async def update_user_profile(username: str, user: UserProfile):
    """Update the user profile (movie list)."""
    conn = get_db_connection()
    cursor = conn.cursor()

    # Check if the user exists
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    existing_user = cursor.fetchone()

    if not existing_user:
        raise HTTPException(status_code=404, detail="User not found")

    user_id = existing_user["user_id"]

    # Delete existing movie list and update it
    cursor.execute("DELETE FROM user_movie_list WHERE user_id = ?", (user_id,))

    # Add new movie list for the user
    for movie in user.liked_movies:
        cursor.execute("INSERT INTO user_movie_list (user_id, movie_title) VALUES (?, ?)", (user_id, movie))

    conn.commit()
    conn.close()

    return user

@app.delete("/user/{username}")
async def delete_user(username: str):
    """Delete the user and their movie list."""
    conn = get_db_connection()
    cursor = conn.cursor()

    # Check if the user exists
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    user = cursor.fetchone()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user_id = user["user_id"]

    # Delete the user and their movie list
    cursor.execute("DELETE FROM user_movie_list WHERE user_id = ?", (user_id,))
    cursor.execute("DELETE FROM users WHERE user_id = ?", (user_id,))

    conn.commit()
    conn.close()

    return {"message": "User and movie list deleted successfully"}

@app.post("/recommend", response_model=RecommendationResponse)
async def recommend(request: RecommendRequest):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users WHERE username = ?", (request.username,))
    user = cursor.fetchone()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user_id = user["user_id"]

    cursor.execute("SELECT movie_title FROM user_movie_list WHERE user_id = ?", (user_id,))
    liked_movies = [row["movie_title"] for row in cursor.fetchall()]
    conn.close()

    if not liked_movies:
        raise HTTPException(status_code=400, detail="User has not liked any movies yet")

    movie_scores = recommend_movies(movie_df=movie_df, user_liked_movies=liked_movies, matrix=tfidf_matrix if request.method == 'tfidf' else count_matrix, count=request.no_of_recommendations)

    # liked_movie_indices = movie_df[movie_df['title'].isin(liked_movies)].index
    # if request.method == "tfidf":
    #     liked_movie_vectors = tfidf_matrix[liked_movie_indices]
    #     user_profile_vector = np.asarray(liked_movie_vectors.mean(axis=0)).reshape(1, -1)
    #     similarity_matrix = tfidf_matrix
    # else:
    #     liked_movie_vectors = count_matrix[liked_movie_indices]
    #     user_profile_vector = np.asarray(liked_movie_vectors.mean(axis=0)).reshape(1, -1)
    #     similarity_matrix = count_matrix

    # user_similarities = cosine_similarity(user_profile_vector, similarity_matrix).flatten()
    # movie_df["similarity"] = user_similarities
    # recommendations = movie_df.sort_values(by="similarity", ascending=False).head(request.no_of_recommendations)[["title", "similarity"]]
    accuracies = test_accuracy(movie_df=movie_df,
                  recommended_movies=movie_scores,
                  user_liked_movies=liked_movies,
                  vectorizer=tfidf_vectorizer if request.method == 'tfidf' else count_vectorizer)
    # recommended_set = set(movie_scores["title"])
    # actual_set = set(liked_movies)
    # TP = len(recommended_set & actual_set)
    # FP = len(recommended_set - actual_set)
    # FN = len(actual_set - recommended_set)

    # precision = TP / (TP + FP) if (TP + FP) > 0 else 0
    # recall = TP / (TP + FN) if (TP + FN) > 0 else 0
    # f1 = (2 * precision * recall) / (precision + recall) if (precision + recall) > 0 else 0

    return RecommendationResponse(
        precision=accuracies['precision'],
        recall=accuracies['recall'],
        f1_score=accuracies['f1_score'],
        text_similarity_score=accuracies['text_similarity_score'],
        recommendations=[MovieRecommendation(**row) for _, row in movie_scores.iterrows()]
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000)