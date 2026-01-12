import os
import sys
import pandas as pd
from google.cloud import storage
from house_pricing import logger
from house_pricing import custom_exception
from sklearn.model_selection import train_test_split
from house_pricing.config.paths_config import *
from house_pricing.utils import common_functions

logger = logger.get_logger(__name__)

class DataIngestion:
    def __init__(self, config):
        self.config = config["data_ingestion"]
        self.bucket_name = self.config["bucket_name"]
        self.file_name = self.config["bucket_file_name"]
        self.train_ratio = self.config["train_ratio"]
        self.project_id = self.config["project_id"]

        os.makedirs(RAW_DIR, exist_ok=True)

        logger.info("DataIngestion instance created.")

    def download_data(self):
        try:
            if self.project_id:
                client = storage.Client(project=self.project_id)
            else:
                client = storage.Client()
            bucket = client.bucket(self.bucket_name)
            blob = bucket.blob(self.file_name)
            blob.download_to_filename(RAW_FILE_PATH)

            logger.info(f"Data downloaded from bucket {self.bucket_name} to {RAW_FILE_PATH}.")
        except Exception as e:
            logger.error(f"Error downloading data")
            raise custom_exception.CustomException(e, sys)
        
    def split_data(self):
        try:
            logger.info("Starting data split into train and test sets...")
            data=pd.read_csv(RAW_FILE_PATH)
            train_data, test_data = train_test_split(data, test_size=1-self.train_ratio, random_state=42)

            train_data.to_csv(TRAIN_FILE_PATH)
            test_data.to_csv(TEST_FILE_PATH)
            logger.info(f"Data split completed. Train data saved to {TRAIN_FILE_PATH}, Test data saved to {TEST_FILE_PATH}.")
        except Exception as e:
            logger.error(f"Error splitting data")
            raise custom_exception.CustomException(e, sys)
        
    def run(self):
        try:
            self.download_data()
            self.split_data()
            logger.info("Data ingestion process completed successfully.")
        except Exception as e:
            logger.error(f"Error in data ingestion process")
            raise custom_exception.CustomException(e, sys)
        
        finally:
            logger.info("DataIngestion run method finished.")

if __name__ == "__main__":

    data_ingestion = DataIngestion(common_functions.read_yaml_file(CONFIG_PATH))
    data_ingestion.run()