import pickle
from typing import List
import pandas as pd

from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from scipy.sparse import spmatrix
from pathlib import Path
import os, sys
import logging
from fastapi import FastAPI, HTTPException, Depends, Query
from sqlalchemy.orm import Session

from models import User, Movie, UserMovie
from schemas import LikeRequest, MovieCreate, MovieRead, MovieUpdate, LikedMovie, RecommendRequest, MovieRecommendation, RecommendationResponse, UserCreate, UserRead
from ML_pipeline.testing import recommend_movies, test_accuracy
from ML_pipeline.isa_project_1.config import MODELS_DIR
# Seeding the database
from database.config import SessionLocal, engine, Base, was_just_created
from database.seeders import seed_with_dataframe

# Basic config — you can tweak format/level/handlers as you like
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
logger = logging.getLogger(__name__)  # module-level logger

PROJECT_ROOT = Path(os.getcwd()).parent

# # Add it to sys.path
sys.path.append(str(PROJECT_ROOT))

from ML_pipeline.isa_project_1.config import MODELS_DIR
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

movie_df: pd.DataFrame = pd.read_pickle(MODELS_DIR / "movie_df.pkl")


# Initialize DB
Base.metadata.create_all(bind=engine)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



if was_just_created:
    logger.info("Database was just created. Seeding with movie data...")
    # Seed the database with movie data
    seed_with_dataframe(path=MODELS_DIR / "movie_df.pkl")
    logger.info("Database seeded successfully.")

# Load models
# with open(MODELS_DIR / "tfidf_matrix.pkl", "rb") as f:
#     tfidf_matrix: spmatrix = pickle.load(f)
# with open(MODELS_DIR / "count_matrix.pkl", "rb") as f:
#     count_matrix: spmatrix = pickle.load(f)
# movie_df: pd.DataFrame = pd.read_pickle(MODELS_DIR / "movie_df.pkl")

app = FastAPI()


@app.post("/user/", response_model=UserRead)
# async def create_movie(movie_in: MovieCreate, db: Session = Depends(get_db)):
async def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = User(username=user.username)
    db.add(db_user)

    try:
        db.commit()
        db.refresh(db_user)
    except Exception:
        db.rollback()
        raise HTTPException(status_code=409, detail="User already exists")
    # add liked movies
    # for title in user.liked_movies:
    #     um = UserMovie(user_id=db_user.user_id, movie_title=title)
    #     db.add(um)
    # db.commit()
    return db_user

@app.get("/user/all", response_model=List[UserRead])
async def get_all_users(db: Session = Depends(get_db)):
    """Get all users and their movie lists."""

    # Get all users
    db_users = db.query(User).all()

    user_profiles = []
    for user in db_users:
        user_id = user.user_id
        username = user.username

        db_user_movies = db.query(UserMovie).filter(UserMovie.user_id == user_id).all()
        user_profiles.append(UserRead(username=username, liked_movies=[LikedMovie(movie_id=um.movie_id, title=um.movie_title) for um in db_user_movies], user_id=user_id))

    return user_profiles

@app.get("/user/{username}", response_model=UserRead)
def get_user(username: str, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.username == username).first()
    if not db_user:
        raise HTTPException(404, "User not found")
    liked = [LikedMovie(movie_id=um.movie_id, title=um.movie_title) for um in db_user.liked]
    return UserRead(username=username, liked_movies=liked, user_id=db_user.user_id)

@app.post("/recommend", response_model=RecommendationResponse)
def recommend(request: RecommendRequest, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.username == request.username).first()
    if not db_user:
        raise HTTPException(404, "User not found")
    liked = [um.movie_title for um in db_user.liked]

    if not liked:
        raise HTTPException(400, "User has not liked any movies yet")

    # Ensure at least one liked movie exists in our catalog
    present = movie_df['title'].isin(liked)
    if not present.any():
        raise HTTPException(400, "None of the user's liked movies exist in our catalog")
    
    movie_scores = recommend_movies(movie_df, liked,
                                    matrix=tfidf_matrix if request.method=='tfidf' else count_matrix,
                                    count=request.no_of_recommendations)
    accuracies = test_accuracy(movie_df, movie_scores, liked,
                                vectorizer=(tfidf_vectorizer if request.method=='tfidf' else count_vectorizer))
    return RecommendationResponse(
        precision=accuracies['precision'],
        recall=accuracies['recall'],
        f1_score=accuracies['f1_score'],
        recommendations=[MovieRecommendation(**row) for _, row in movie_scores.iterrows()]
    )


@app.post("/movies/", response_model=MovieRead)
def create_movie(movie_in: MovieCreate, db: Session = Depends(get_db)):
    db_movie = Movie(title=movie_in.title)
    db.add(db_movie)
    db.commit()
    db.refresh(db_movie)
    return db_movie

@app.get("/movies/", response_model=list[MovieRead])
def list_movies(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    movies = db.query(Movie).offset(skip).limit(limit).all()
    return movies

@app.get("/movies/{movie_id}", response_model=MovieRead)
def get_movie(movie_id: int, db: Session = Depends(get_db)):
    movie = db.query(Movie).filter(Movie.movie_id == movie_id).first()
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    return movie

@app.put("/movies/{movie_id}", response_model=MovieRead)
def update_movie(movie_id: int, movie_in: MovieUpdate, db: Session = Depends(get_db)):
    movie = db.query(Movie).filter(Movie.movie_id == movie_id).first()
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    movie.title = movie_in.title
    db.commit()
    db.refresh(movie)
    return movie

@app.delete("/movies/{movie_id}", status_code=204)
def delete_movie(movie_id: int, db: Session = Depends(get_db)):
    movie = db.query(Movie).filter(Movie.movie_id == movie_id).first()
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    db.delete(movie)
    db.commit()
    return


@app.post("/movies/like")
def like_movie(request: LikeRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == request.username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    movie = db.query(Movie).filter(Movie.movie_id == request.movie_id).first()
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")

    # Check if already liked
    existing = db.query(UserMovie).filter_by(user_id=user.user_id, movie_title=movie.title).first()
    if existing:
        raise HTTPException(status_code=400, detail="Movie already liked")

    user_movie = UserMovie(
        user_id=user.user_id,
        movie_title=movie.title,
        movie_id=movie.movie_id
    )
    db.add(user_movie)
    db.commit()
    return {"message": f"{user.username} liked '{movie.title}'"}

@app.post("/movies/dislike")
def dislike_movie(request: LikeRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == request.username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    movie = db.query(Movie).filter(Movie.movie_id == request.movie_id).first()
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")

    # Find and delete the relationship
    user_movie = db.query(UserMovie).filter_by(user_id=user.user_id, movie_title=movie.title).first()
    if not user_movie:
        raise HTTPException(status_code=400, detail="Movie not liked yet")

    db.delete(user_movie)
    db.commit()
    return {"message": f"{user.username} disliked '{movie.title}'"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000)