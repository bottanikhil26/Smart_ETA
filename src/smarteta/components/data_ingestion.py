from src.smarteta.exception.exception import SmartetaException
from src.smarteta.logging.logger import logging
from src.smarteta.config.configuration import DataIngestionConfig
from src.smarteta.entity.artifact_entity import DataIngestionArtifact
import os
import sys
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import pandas as pd
import numpy as np
from typing import List
from sklearn.model_selection import train_test_split

from dotenv import load_dotenv
load_dotenv()
MONGO_DB_URL = os.getenv("MONGO_DB_URL")

class DataIngestion:
    """
    This class is used to define the data ingestion process.
    """

    def __init__(self, data_ingestion_config: DataIngestionConfig):
        try:
            self.data_ingestion_config = data_ingestion_config
        except Exception as e:
            raise SmartetaException(e, sys) from e
        
    
    def export_collection_as_dataframe(self) -> pd.DataFrame:
        """
        This method exports the MongoDB collection as a pandas DataFrame.
        """
        try:
            self.client = MongoClient(MONGO_DB_URL, server_api=ServerApi('1'))
            self.database = self.client[self.data_ingestion_config.data_ingestion_database_name]
            self.collection = self.database[self.data_ingestion_config.data_ingestion_collection_name]

            df = pd.DataFrame(list(self.collection.find()))

            if "_id" in df.columns:
                df.drop(columns=['_id'], axis=1, inplace=True)
            
            df = df.apply(lambda x: x.str.strip() if x.dtype == "object" else x)
            for col in df.select_dtypes(include=["object"]).columns:
                df[col] = df[col].replace(["NaN", "nan", "null", "NULL", "", "NA", "N/A", "--"], np.nan)
            return df
        except Exception as e:
            raise SmartetaException(e, sys) from e
        
    def export_data_to_feature_store(self, dataframe: pd.DataFrame):
        """
        This method exports the DataFrame to the feature store.
        """
        try:
            feature_store_file_path = self.data_ingestion_config.data_ingestion_feature_store_file_path
            dir_path = os.path.dirname(feature_store_file_path)
            os.makedirs(dir_path, exist_ok=True)
            dataframe.to_csv(feature_store_file_path, index=False,header=True)
            return dataframe
        except Exception as e:
            raise SmartetaException(e, sys) from e
        
    def split_data_as_train_test(self, dataframe: pd.DataFrame) -> List[pd.DataFrame]:
        """
        This method splits the DataFrame into training and testing sets.
        """
        try:
            train_set, test_set = train_test_split(dataframe, test_size=self.data_ingestion_config.data_ingestion_train_test_split_ratio,random_state=42)
            dir_path = os.path.dirname(self.data_ingestion_config.data_ingestion_train_file_path)
            
            os.makedirs(dir_path, exist_ok=True)
            
            logging.info(f"Exporting train and test file path.")
            
            train_set.to_csv(
                self.data_ingestion_config.data_ingestion_train_file_path, index=False, header=True
            )

            test_set.to_csv(
                self.data_ingestion_config.data_ingestion_test_file_path, index=False, header=True
            )
            logging.info(f"Exported train and test file path.")
        except Exception as e:
            raise SmartetaException(e, sys) from e

        
    def initiate_data_ingestion(self):
        """
        This method initiates the data ingestion process.
        """
        try:
            dataframe = self.export_collection_as_dataframe()
            dataframe = self.export_data_to_feature_store(dataframe=dataframe)
            self.split_data_as_train_test(dataframe)
            dataingestionartifact = DataIngestionArtifact(train_file_path =self.data_ingestion_config.data_ingestion_train_file_path,
                                                          test_file_path =self.data_ingestion_config.data_ingestion_test_file_path)
            return dataingestionartifact
        except Exception as e:
            raise SmartetaException(e, sys) from e
