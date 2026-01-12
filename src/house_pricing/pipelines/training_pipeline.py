from house_pricing.components import data_ingestion
from house_pricing.components import data_processing
from house_pricing.components import model_training
from house_pricing.utils import common_functions
from house_pricing.config import paths_config



if __name__ == "__main__":
    ## Data Ingestion
    data_ingestion = data_ingestion.DataIngestion(common_functions.read_yaml_file(paths_config.CONFIG_PATH))
    data_ingestion.run()

    ## Data Processing
    processor = data_processing.DataProcessor(paths_config.TRAIN_FILE_PATH, paths_config.TEST_FILE_PATH, paths_config.PROCESSED_DIR, paths_config.CONFIG_PATH)
    processor.process()

    ## Model Training 

    trainer = model_training.ModelTraining(train_path=paths_config.PROCESSED_TRAIN_FILE_PATH, test_path=paths_config.PROCESSED_TEST_FILE_PATH, model_output_path=paths_config.MODEL_OUTPUT_PATH)
    trainer.run()