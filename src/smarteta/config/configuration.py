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
        self.model_dir=os.path.join("final_model")
        self.artifact_dir = os.path.join( self.artifact_name,self.time_stamp)

class DataIngestionConfig:
    """
    This class is used to define the configuration for data ingestion.
    """

    def __init__(self, pipeline_config: TrainingPipelineConfig):
        self.data_ingestion_dir :str = os.path.join(pipeline_config.artifact_dir, constants.DATA_INGESTION_DIR_NAME)
        self.data_ingestion_collection_name : str = constants.DATA_INGESTION_COLLECTION_NAME
        self.data_ingestion_database_name : str = constants.DATA_INGESTION_DATABASE_NAME
        self.data_ingestion_feature_store_file_path :str  = os.path.join(self.data_ingestion_dir, constants.DATA_INGESTION_FEATURE_STORE_DIR,constants.FILE_NAME)
        self.data_ingestion_train_file_path : str = os.path.join(self.data_ingestion_dir, constants.DATA_INGESTION_INGESTED_DIR, constants.TRAIN_FILE_NAME)
        self.data_ingestion_test_file_path : str = os.path.join(self.data_ingestion_dir, constants.DATA_INGESTION_INGESTED_DIR, constants.TEST_FILE_NAME)
        self.data_ingestion_train_test_split_ratio : float = constants.DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO


class DataValidationConfig:
    """
    This class is used to define the configuration for data validation.
    """

    def __init__(self, pipeline_config: TrainingPipelineConfig):
        self.data_validation_dir :str = os.path.join(pipeline_config.artifact_dir, constants.DATA_VALIDATION_DIR_NAME)
        self.data_validation_valid_dir : str = os.path.join(self.data_validation_dir, constants.DATA_VALIDATION_VALID_DIR)
        self.data_validation_invalid_dir : str = os.path.join(self.data_validation_dir, constants.DATA_VALIDATION_INVALID_DIR)
        self.valid_train_file_path : str = os.path.join(self.data_validation_valid_dir, constants.TRAIN_FILE_NAME)
        self.valid_test_file_path : str = os.path.join(self.data_validation_valid_dir, constants.TEST_FILE_NAME)
        self.invalid_train_file_path : str = os.path.join(self.data_validation_invalid_dir, constants.TRAIN_FILE_NAME)
        self.invalid_test_file_path : str = os.path.join(self.data_validation_invalid_dir, constants.TEST_FILE_NAME)
        self.drift_report_file_path: str = os.path.join(
            self.data_validation_dir,
            constants.DATA_VALIDATION_DRIFT_REPORT_DIR,
            constants.DATA_VALIDATION_DRIFT_REPORT_FILE_NAME,
        )

class DataTransformationConfig:
     def __init__(self,training_pipeline_config:TrainingPipelineConfig):
        self.data_transformation_dir: str = os.path.join( training_pipeline_config.artifact_dir,constants.DATA_TRANSFORMATION_DIR_NAME )
        self.transformed_train_file_path: str = os.path.join( self.data_transformation_dir,constants.DATA_TRANSFORMATION_TRANSFORMED_DIR,
            constants.TRAIN_FILE_NAME)
        self.transformed_test_file_path: str = os.path.join(self.data_transformation_dir,  constants.DATA_TRANSFORMATION_TRANSFORMED_DIR,
            constants.TEST_FILE_NAME )
        self.transformed_object_file_path: str = os.path.join( self.data_transformation_dir, constants.DATA_TRANSFORMATION_TRANSFORMED_OBJECT_DIR,
            constants.PREPROCESSING_OBJECT_FILE_NAME,)