from pathlib import Path

from dotenv import load_dotenv
from loguru import logger

# Load environment variables from .env file if it exists
load_dotenv()

# Paths
PROJ_ROOT = Path(__file__).resolve().parents[1]
logger.info(f"PROJ_ROOT path is: {PROJ_ROOT}")

DATA_DIR = PROJ_ROOT / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
INTERIM_DATA_DIR = DATA_DIR / "interim"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
EXTERNAL_DATA_DIR = DATA_DIR / "external"

MODELS_DIR = PROJ_ROOT / "models"

REPORTS_DIR = PROJ_ROOT / "reports"
FIGURES_DIR = REPORTS_DIR / "figures"


# Define directories for storing raw and processed data
DOWLOADED_DATASET_DIR = Path(RAW_DATA_DIR / 'ibmd')  # Directory where the downloaded dataset will be stored
PROCESSED_DATASET_DIR = Path(INTERIM_DATA_DIR / 'ibmd')  # Directory where the processed dataset will be saved

DATASETS = {
    'tmdb_5000_movies.csv': PROCESSED_DATASET_DIR / 'processed_movies.csv',
    'tmdb_5000_credits.csv': PROCESSED_DATASET_DIR / 'processed_credits.csv'
}


# If tqdm is installed, configure loguru with tqdm.write
# https://github.com/Delgan/loguru/issues/135
try:
    from tqdm import tqdm

    logger.remove(0)
    logger.add(lambda msg: tqdm.write(msg, end=""), colorize=True)
except ModuleNotFoundError:
    pass
