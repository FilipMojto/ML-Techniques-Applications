from pathlib import Path

import typer
from loguru import logger
from tqdm import tqdm

from isa_project_1.config import PROCESSED_DATA_DIR

app = typer.Typer()

from dataset import MOVIE_DATASET_CSV, CREDIT_DATASET_CSV, INPUT_OUTPUT_MAPPING

SELECTED_DF = INPUT_OUTPUT_MAPPING[MOVIE_DATASET_CSV]


@app.command()
def main(
    # ---- REPLACE DEFAULT PATHS AS APPROPRIATE ----
    input_path: Path = PROCESSED_DATA_DIR / "dataset.csv",
    output_path: Path = PROCESSED_DATA_DIR / "features.csv",
    # -----------------------------------------
):
    # ---- REPLACE THIS WITH YOUR OWN CODE ----
    logger.info("Generating features from dataset...")
    for i in tqdm(range(10), total=10):
        if i == 5:
            logger.info("Something happened for iteration 5.")
    logger.success("Features generation complete.")
    # -----------------------------------------


if __name__ == "__main__":
    app()
