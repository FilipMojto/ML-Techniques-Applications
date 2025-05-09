from pydantic import BaseModel
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

class Profile(BaseModel):
    liked_movies: List[str]

class UserProfile(Profile):
    username: str


class MovieCreate(BaseModel):
    title: str

class MovieRead(BaseModel):
    movie_id: int
    title: str

    class Config:
        orm_mode = True

class MovieUpdate(BaseModel):
    title: str

class LikeRequest(BaseModel):
    username: str
    movie_id: int