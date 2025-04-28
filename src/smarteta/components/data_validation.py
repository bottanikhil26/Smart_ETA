from src.smarteta.entity.artifact_entity import DataIngestionArtifact, DataValidationArtifact
from src.smarteta.config.configuration import DataValidationConfig
from src.smarteta.exception.exception import SmartetaException
from src.smarteta.logging.logger import logging
from src.smarteta.constants import SCHEMA_FILE_PATH
from scipy.stats import ks_2samp
import pandas as pd
import os
import sys
from src.smarteta.utils.common import read_yaml_file, write_yaml_file

class DataValidation:
    """
    This class is used to define the data validation process.
    """
    def __init__(self, data_validation_config: DataValidationConfig,
                 data_ingestion_artifact: DataIngestionArtifact):
        try:
            self.data_validation_config = data_validation_config
            self.data_ingestion_artifact = data_ingestion_artifact
            self.schema_config = read_yaml_file(SCHEMA_FILE_PATH)
        except Exception as e:
            raise SmartetaException(e, sys) from e

    @staticmethod    
    def read_data( file_path: str) -> pd.DataFrame:
        """
        This method reads the data from the given file path.
        """
        try:
            df = pd.read_csv(file_path)
            return df
        except Exception as e:
            raise SmartetaException(e, sys) from e
    
    def validate_number_of_columns(self, dataframe: pd.DataFrame) -> bool:
        try:
            number_of_columns = len(self.schema_config['columns'])
            logging.info(f"required number of columns: {number_of_columns}")
            logging.info(f"actual number of columns: {dataframe.columns}")
            if len(dataframe.columns) == number_of_columns:
                logging.info("Number of columns are valid")
                return True
            else:
                logging.info("Number of columns are not valid")
                return False
        except Exception as e:
            raise SmartetaException(e, sys) from e
        
    def detect_data_drift(self, base_df: pd.DataFrame, current_df: pd.DataFrame,threshold=0.05) -> bool:
        try:
            status = True
            report = {}
            for column in base_df.columns:
                d1 = base_df[column]
                d2 = current_df[column]
                ks_test_result = ks_2samp(d1, d2)
                if threshold <= ks_test_result.pvalue:
                    is_found_drift = False
                else :
                    is_found_drift = True
                    status = False
                report.update({column: {
                    "p_value": float(ks_test_result.pvalue),
                    "is_found_drift": is_found_drift
                }})
            drift_report_file_path = self.data_validation_config.drift_report_file_path
            dir_path = os.path.dirname(drift_report_file_path)
            os.makedirs(dir_path, exist_ok=True)
            write_yaml_file(drift_report_file_path, report, replace=True)
        except Exception as e:  
            raise SmartetaException(e, sys) from e

    def initiate_data_validation(self)->DataValidationArtifact:
        try:
            train_file_path = self.data_ingestion_artifact.train_file_path
            test_file_path = self.data_ingestion_artifact.test_file_path

            train_data = DataValidation.read_data(train_file_path)
            test_data = DataValidation.read_data(test_file_path)

            #valid number of columns
            status = self.validate_number_of_columns(train_data)
            if not status:
                error_message = f"Train data does not contain all the required columns/n" 
        
            status = self.validate_number_of_columns(test_data)
            if not status:
                error_message =f"Test data does not contain all the required columns/n"
            
            new_status = self.detect_data_drift(train_data, test_data)
            if status:
                dir_path = os.path.dirname(self.data_validation_config.valid_train_file_path)
                os.makedirs(dir_path, exist_ok=True)

                logging.info("Data is valid")
            
                train_data.to_csv(self.data_validation_config.valid_train_file_path, index=False, header=True)

            
                test_data.to_csv(self.data_validation_config.valid_test_file_path, index=False, header=True)
            else :
                dir_path = os.path.dirname(self.data_validation_config.invalid_train_file_path)
                os.makedirs(dir_path, exist_ok=True)
                logging.info("Data is not valid")
                train_data.to_csv(self.data_validation_config.invalid_train_file_path, index=False, header=True)
                test_data.to_csv(self.data_validation_config.invalid_test_file_path, index=False, header=True)
                error_message =f"{error_message} : Data drift is found/n"
                status = False
            
            data_validation_artifact = DataValidationArtifact(
                validation_status=new_status,
                valid_train_file_path=self.data_validation_config.valid_train_file_path,
                valid_test_file_path=self.data_validation_config.valid_test_file_path,
                invalid_train_file_path=self.data_validation_config.invalid_train_file_path,
                invalid_test_file_path=self.data_validation_config.invalid_test_file_path,
                drift_report_file_path=self.data_validation_config.drift_report_file_path
            )
        except Exception as e:
            raise SmartetaException(e, sys) from e
        
    