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
            
            df.replace({'na':np.nan}, inplace=True)
            return df
        except Exception as e:
            raise SmartetaException(e, sys) from e
        
    def export_data_to_feature_store(self, dataframe: pd.DataFrame):
        """
        This method exports the DataFrame to the feature store.
        """
        try:
            feature_store_file_path = self.data_ingestion_config.data_ingestion_feature_store_dir
            dir_path = os.path.dirname(feature_store_file_path)
            os.makedirs(dir_path, exist_ok=True)
            dataframe.to_csv(feature_store_file_path, index=False,header=True)
            return dataframe
        except Exception as e:
            raise SmartetaException(e, sys) from e

        
    def initiate_data_ingestion(self):
        """
        This method initiates the data ingestion process.
        """
        try:
            dataframe = self.export_collection_as_dataframe()
            dataframe = self.export_data_to_feature_store(dataframe=dataframe)
            dataingestionartifact = DataIngestionArtifact(file_path =self.data_ingestion_config.data_ingestion_feature_store_dir)
            return dataingestionartifact
        except Exception as e:
            raise SmartetaException(e, sys) from e
