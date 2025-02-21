# Importing required libraries
from pathlib import Path  # For file path operations
from kagglehub import dataset_download  # To download datasets from Kaggle
import typer  # For creating the command-line interface
from loguru import logger  # For logging
from tqdm import tqdm  # For displaying progress bars
import pandas as pd  # For data manipulation (pandas DataFrame)
from isa_project_1.config import DOWLOADED_DATASET_DIR, PROCESSED_DATASET_DIR, DATASETS  # Custom config module
from shutil import move  # To move files from one location to another

# Initialize the Typer application (for CLI commands)
app = typer.Typer()


def download_dataset(dir: Path = DOWLOADED_DATASET_DIR):
    """
    Downloads the movie metadata dataset from Kaggle, and moves it to the specified directory.
    
    :param dir: The directory where the downloaded dataset will be moved. Default is DOWLOADED_DATASET_DIR.
    """
    logger.info("Starting download...")  # Log that the download is starting
    downloaded_path = dataset_download("tmdb/tmdb-movie-metadata")  # Download the dataset from Kaggle
    logger.info("Download complete!")  # Log that the download is complete

    # Move the downloaded file to the desired directory
    move(downloaded_path, dir)  
    logger.success(f"Dataset saved to: {dir}")  # Log the successful move of the dataset
    print("Path to dataset files:", dir)  # Print the directory path where the dataset is saved

# Default dataset selection for movie dataset
# SELECTED_MOVIE_DATASET = MOVIE_DATASET_CSV

@app.command()  # The main function will be exposed as a CLI command
def main(
    # input_path: Path = SELECTED_MOVIE_DATASET,  # Default input path is the selected movie dataset
    # output_path: Path = INPUT_OUTPUT_MAPPING[SELECTED_MOVIE_DATASET],  # Default output path based on input path mapping
):
    """
    Main function to handle the dataset processing.
    - If the dataset doesn't exist locally, it will attempt to download it.
    - If the output directory doesn't exist, it will be created.
    - The dataset is read, processed, and saved to a new location.
    
    :param input_path: Path to the input dataset (CSV file).
    :param output_path: Path to save the processed dataset (CSV file).
    """
    for dataset, output_path in DATASETS.items():
        logger.info(f"Processing dataset: `{dataset}`")
        # Simulate a processing loop with progress bar
        for i in tqdm(range(10), total=10):  # For each iteration, display progress
            if i == 0:
                logger.info("Checking dependency paths...")
                dataset_path = DOWLOADED_DATASET_DIR / dataset
                
                # Check if the dataset exists locally, if not, download it
                if not dataset_path.exists():
                    logger.info("Dataset not found locally! Attempting to download...")
                    download_dataset()  # Call the function to download the dataset

                # Check if the output directory exists, if not, create it
                if not Path(PROCESSED_DATASET_DIR).exists():
                    logger.info("Output directory doesn't exist. Creating new...")
                    Path(PROCESSED_DATASET_DIR).mkdir(parents=True, exist_ok=True)  # Create the directory if it doesn't exist
                    logger.info("Done!")  # Log that the directory creation is done
            elif i == 1:
                # Data processing logic starts here
                logger.info("Processing dataset...")  # Log that the dataset processing has started
                logger.info("Opening dataset in Pandas...")  # Log that the dataset is being loaded into a pandas DataFrame

                df = pd.read_csv(dataset_path)  # Load the dataset into a pandas DataFrame
                logger.info("Success!")  # Log successful loading of the dataset
            elif i == 2:
                logger.info("Saving the processed dataset...")  # Log that the processed dataset is being saved
                df.to_csv(output_path, index=False)  # Save the processed DataFrame to a CSV file
            elif i == 3:
                logger.success("Processing dataset complete.")  # Log the successful completion of the processing


# This runs the application if the script is executed directly (CLI entry point)
if __name__ == "__main__":
    app()  # Run the Typer app (CLI)
