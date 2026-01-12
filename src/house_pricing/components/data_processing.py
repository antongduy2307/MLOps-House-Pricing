import os
import sys
import pandas as pd
import numpy as np
from house_pricing import logger
from house_pricing import custom_exception
from house_pricing.config import paths_config
from house_pricing.utils import common_functions
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from imblearn.over_sampling import SMOTE

logger = logger.get_logger(__name__)

class DataProcessor:
    def __init__(self, train_path, test_path, processed_dir, config_path):
        self.train_path = train_path
        self.test_path = test_path
        self.processed_dir = processed_dir
        self.config = common_functions.read_yaml_file(config_path)

        os.makedirs(self.processed_dir, exist_ok=True)

    def preprocess_data(self, df):
        try:
            logger.info("Starting preprocessing data...")
            logger.info("Dropping columns...")
            df.drop(columns=['Unnamed: 0', 'Booking_ID'], inplace=True)
            df.drop_duplicates(inplace=True)

            cat_cols = self.config['data_processing']['categorical_columns']
            num_cols = self.config['data_processing']['numerical_columns']

            logger.info("Encoding categorical columns...")
            label_encoder = LabelEncoder()
            mappings={}
            for col in cat_cols:
                df[col] = label_encoder.fit_transform(df[col])
                mappings[col] = {label:code for label,code in zip(label_encoder.classes_ , label_encoder.transform(label_encoder.classes_))}
            for col, mapping in mappings.items():
                logger.info(f"Mapping for {col}: {mapping}")
    
            logger.info("Handling skewness...")
            skewness_threshold = self.config['data_processing']['skewness_threshold']
            skewness = df[num_cols].apply(lambda x: x.skew())
            for column in skewness[skewness > skewness_threshold].index:
                df[column] = np.log1p(df[column])
            return df

        except Exception as e:
            logger.error(f"Error in preprocessing data: {e}")
            raise custom_exception.CustomException(e, sys)
        
    def balance_data(self, df):
        try:
            logger.info("Balancing data...")
            X = df.drop(columns=['booking_status'])
            y = df['booking_status']

            smote = SMOTE(random_state=42)
            X_res, y_res = smote.fit_resample(X, y)

            balanced_df = pd.DataFrame(X_res, columns=X.columns) 
            balanced_df['booking_status'] = y_res

            logger.info("Data balanced successfully")
            return balanced_df
        except Exception as e:
            logger.error(f"Error in balancing data: {e}")
            raise custom_exception.CustomException(e, sys)
        
    def feature_selection(self, df):
        try:
            logger.info("Starting feature selection")
            X = df.drop(columns='booking_status')
            y = df["booking_status"]
            
            model = RandomForestClassifier(random_state=42)
            model.fit(X,y)

            feature_importance = model.feature_importances_

            feature_importance_df = pd.DataFrame({
                'feature':X.columns,
                'importance':feature_importance
            })

            top_features_importance_df = feature_importance_df.sort_values(by="importance" , ascending=False)

            number_features_to_select = self.config["data_processing"]["number_of_features"]

            top_10_features = top_features_importance_df["feature"].head(number_features_to_select).values

            top_10_df = df[top_10_features.tolist() + ["booking_status"]]

            logger.info("Feature selection completed!")

            return top_10_df
        
        except Exception as e:
            logger.error(f"Error in feature selection step: {e}")
            raise custom_exception.CustomException(e, sys)
        
    def save_data(self, df, file_path):
        try:
            logger.info("Saving data in processed folder ...")
            df.to_csv(file_path, index = False)
            logger.info("Saving data successfully")
        except Exception as e:
            logger.error(f"Error in saving data: {e}")
            raise custom_exception.CustomException(e, sys)

    def process(self):
        try:
            logger.info("Loading the data from raw dir ...")
            train_df = common_functions.load_data(self.train_path)
            test_df = common_functions.load_data(self.test_path)

            train_df = self.preprocess_data(train_df)
            test_df = self.preprocess_data(test_df)

            train_df = self.balance_data(train_df)
            test_df = self.balance_data(test_df)

            train_df = self.feature_selection(train_df)
            test_df = test_df[train_df.columns]

            self.save_data(train_df, paths_config.PROCESSED_TRAIN_FILE_PATH)
            self.save_data(test_df, paths_config.PROCESSED_TEST_FILE_PATH)

            logger.info("Data process complete successfully!")

        except Exception as e:
            logger.error(f"Error in preprocessing pipeline : {e}")
            raise custom_exception.CustomException(e, sys)

if __name__=="__main__":
    processor = DataProcessor(paths_config.TRAIN_FILE_PATH, paths_config.TEST_FILE_PATH, paths_config.PROCESSED_DIR, paths_config.CONFIG_PATH)
    processor.process()