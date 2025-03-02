from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Optional
import pickle
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
from scipy.sparse import spmatrix
import numpy as np
import sqlite3
from pathlib import Path
import os, sys

PROJECT_ROOT = Path(os.getcwd()).parent  # Assuming 'notebooks/' is inside the project root

# Add it to sys.path
sys.path.append(str(PROJECT_ROOT))

from ML_pipeline.isa_project_1.config import MODELS_DIR, PROCESSED_DATA_DIR



# from isa_project_1.config import PROCESSED_DATA_DIR, MODELS_DIR  # Custom config module

# Load the stored TF-IDF data
with open(MODELS_DIR / "tfidf_matrix.pkl", "rb") as f:
    tfidf_matrix: spmatrix = pickle.load(f)

with open(MODELS_DIR / "tfidf_vectorizer.pkl", "rb") as f:
    tfidf_vectorizer: TfidfVectorizer = pickle.load(f)

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
    # liked_movies: List[str]
    no_of_recommendations: int = 10  # Default is 10 recommendations

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
    cursor.execute("INSERT INTO users (username) VALUES (?)", (user.username,))
    user_id = cursor.lastrowid

    # Add user's liked movies to the user_movie_list table
    for movie in user.liked_movies:
        cursor.execute("INSERT INTO user_movie_list (user_id, movie_title) VALUES (?, ?)", (user_id, movie))

    conn.commit()
    conn.close()

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
    """
    Recommend movies based on user's liked movies from the database.
    Accepts the username and returns the top recommendations
    based on content similarity.
    """
    # Get the user profile from the database
    conn = get_db_connection()
    cursor = conn.cursor()

    # Get user info from the request
    cursor.execute("SELECT * FROM users WHERE username = ?", (request.username,))
    user = cursor.fetchone()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user_id = user["user_id"]

    # Get the user's movie list from the database
    cursor.execute("SELECT movie_title FROM user_movie_list WHERE user_id = ?", (user_id,))
    liked_movies = [row["movie_title"] for row in cursor.fetchall()]

    conn.close()

    # Ensure there are liked movies to recommend from
    if not liked_movies:
        raise HTTPException(status_code=400, detail="User has not liked any movies yet")

    # Convert user liked movies into a TF-IDF vector
    liked_movie_indices = movie_df[movie_df['title'].isin(liked_movies)].index
    liked_movie_vectors = tfidf_matrix[liked_movie_indices]  # Subset of tfidf_matrix for liked movies

    # Compute user profile vector as the average of liked movie vectors
    user_profile_vector = np.asarray(liked_movie_vectors.mean(axis=0)).reshape(1, -1)

    # Compute similarity of the user profile with all movies in the dataset
    user_similarities = cosine_similarity(user_profile_vector, tfidf_matrix).flatten()

    # Rank & return top recommendations based on user similarity
    movie_df["similarity"] = user_similarities
    recommendations = movie_df.sort_values(by="similarity", ascending=False).head(request.no_of_recommendations)[["title", "similarity"]]

    # Get recommended movie titles and calculate evaluation metrics
    recommended_set = set(recommendations["title"])
    actual_set = set(liked_movies)

    # Calculate True Positives, False Positives, and False Negatives
    TP = len(recommended_set & actual_set)  # Intersection: movies both recommended and liked
    FP = len(recommended_set - actual_set)  # Recommended but not liked
    FN = len(actual_set - recommended_set)  # Liked but not recommended

    # Compute precision, recall, and F1-score
    precision = TP / (TP + FP) if (TP + FP) > 0 else 0
    recall = TP / (TP + FN) if (TP + FN) > 0 else 0
    f1 = (2 * precision * recall) / (precision + recall) if (precision + recall) > 0 else 0

    # Return the response with evaluation metrics and movie recommendations
    return RecommendationResponse(
        precision=precision,
        recall=recall,
        f1_score=f1,
        recommendations=[MovieRecommendation(**row) for _, row in recommendations.iterrows()]
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000)