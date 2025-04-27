from src.smarteta.exception.exception import SmartetaException
from src.smarteta.logging.logger import logging
from src.smarteta.components.data_ingestion import DataIngestion
from src.smarteta.config.configuration import DataIngestionConfig
from src.smarteta.config.configuration import TrainingPipelineConfig
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
        logging.info("Successfully completed the data ingestion")
        print(data_ingestion_artifact)
    except Exception as e:
        raise SmartetaException(e, sys) from e