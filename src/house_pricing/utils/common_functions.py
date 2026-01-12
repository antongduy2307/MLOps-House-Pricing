import os
import pandas as pd
from house_pricing import logger
from house_pricing import custom_exception
import yaml
import sys

logger = logger.get_logger(__name__)

def read_yaml_file(file_path):
    try:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"The file {file_path} does not exist.")
        
        with open(file_path, 'r') as file:
            content = yaml.safe_load(file)
        logger.info(f"YAML file {file_path} read successfully.")
        return content
    
    except Exception as e:
        logger.error(f"Error reading YAML file {file_path}: {e}")
        raise custom_exception.CustomException(e, sys)

def load_data(path):
    try:
        logger.info(f"Loading data from {path}")
        return pd.read_csv(path)
    except Exception as e:
        logger.error(f"Error loading data from {path}: {e}")
        raise custom_exception.CustomException(e, sys)