import pandas as pd

from ML_pipeline.isa_project_1.config import MODELS_DIR
from models import Movie

from database.config import SessionLocal

def seed_with_dataframe(path: str):
    """
    Seed the database with movie data from a DataFrame.
    This function reads a DataFrame containing movie data and populates the database with it.
    """

    df = pd.read_pickle(path)
    db = SessionLocal()


    for _, row in df.iterrows():
        movie = Movie(title=row['title'])
        db.add(movie)
    
    db.commit()
    db.close()
    print("Database seeded with movie data.")
        