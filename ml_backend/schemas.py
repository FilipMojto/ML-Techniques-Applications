from pydantic import BaseModel, Field
from typing import List, Literal

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

# class Profile(BaseModel):
#     liked_movies: List[str]

# class UserProfile(Profile):
#     username: str


class UserCreate(BaseModel):
    username: str

# Setting orm_mode = True tells Pydantic to accept ORM objects (like SQLAlchemy models) — not just standard Python dictionaries
# and to convert them to dictionaries when serializing.
# This is useful when you want to return SQLAlchemy models directly from your FastAPI endpoints.
class UserRead(UserCreate):
    user_id: int
    liked_movies: List[str] = Field(default_factory=list)


    class Config:
        orm_mode = True

class MovieCreate(BaseModel):
    title: str

class MovieRead(MovieCreate):
    movie_id: int
    # title: str

    class Config:
        orm_mode = True

class MovieUpdate(BaseModel):
    title: str

class LikeRequest(BaseModel):
    username: str
    movie_id: int