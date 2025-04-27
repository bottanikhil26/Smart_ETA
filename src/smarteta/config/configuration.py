from datetime import datetime
import os
import sys
from src.smarteta import constants

class TrainingPipelineConfig:
    """
    This class is used to define the configuration for the training pipeline.
    """

    def __init__(self,time_stamp=datetime.now()):
        time_stamp = time_stamp.strftime("%Y%m%d%H%M%S")
        self.time_stamp = time_stamp
        self.pipeline_name = constants.PIPELINE_NAME
        self.artifact_name = constants.ARTIFACT_DIR
        self.artifact_dir = os.path.join( self.artifact_name,self.time_stamp)

class DataIngestionConfig:
    """
    This class is used to define the configuration for data ingestion.
    """

    def __init__(self, pipeline_config: TrainingPipelineConfig):
        self.data_ingestion_dir :str = os.path.join(pipeline_config.artifact_dir, constants.DATA_INGESTION_DIR_NAME)
        self.data_ingestion_collection_name : str = constants.DATA_INGESTION_COLLECTION_NAME
        self.data_ingestion_database_name : str = constants.DATA_INGESTION_DATABASE_NAME
        self.data_ingestion_feature_store_dir :str  = os.path.join(self.data_ingestion_dir, constants.DATA_INGESTION_FEATURE_STORE_DIR,constants.FILE_NAME)