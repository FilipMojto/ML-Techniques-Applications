# models.py
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database.config import Base

class User(Base):
    __tablename__ = "users"
    user_id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    liked = relationship("UserMovie", back_populates="user", cascade="all, delete-orphan")

class Movie(Base):
    __tablename__ = "movies"
    movie_id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True, nullable=False)
    liked_by = relationship("UserMovie", back_populates="movie", cascade="all, delete-orphan")

class UserMovie(Base):
    __tablename__ = "user_movie_list"
    # Using composite primary key to match existing schema
    user_id = Column(Integer, ForeignKey("users.user_id"), primary_key=True)
    movie_title = Column(String, primary_key=True)
    movie_id = Column(Integer, ForeignKey("movies.movie_id"), nullable=True)

    user = relationship("User", back_populates="liked")
    movie = relationship("Movie", back_populates="liked_by")