from src.smarteta.exception.exception import SmartetaException
from src.smarteta.logging.logger import logging
from src.smarteta.components.data_ingestion import DataIngestion
from src.smarteta.config.configuration import DataIngestionConfig , DataValidationConfig
from src.smarteta.config.configuration import TrainingPipelineConfig
from src.smarteta.components.data_validation import DataValidation
import sys


if __name__ == "__main__":
    try:
        logging.info("Starting the SmartETA pipeline")
        logging.info("Creating the configuration for the training pipeline")
        training_pipeline_config = TrainingPipelineConfig()
        data_ingestion_config = DataIngestionConfig(training_pipeline_config)
        data_ingestion = DataIngestion(data_ingestion_config)
        logging.info("Initiate data ingestion")
        data_ingestion_artifact=data_ingestion.initiate_data_ingestion()
        print(data_ingestion_artifact)
        logging.info("Successfully completed the data ingestion")
        logging.info("Creating the configuration for data validation")
        data_validation_config = DataValidationConfig(training_pipeline_config)
        logging.info("Initiate data validation")
        data_validation = DataValidation(data_validation_config, data_ingestion_artifact)
        logging.info("Exporting the data to feature store")
        data_validation_artifacts=data_validation.initiate_data_validation()
        logging.info("Successfully completed the data validation")
        print(data_validation_artifacts)
    except Exception as e:
        raise SmartetaException(e, sys) from e