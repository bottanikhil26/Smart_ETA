import os
import sys
import pandas as pd
import numpy as np

"""
Defining common constants for the project
"""
TARGET_COLUMN_NAME :str = "Time_taken(min)"
PIPELINE_NAME :str = "SmartETA"
ARTIFACT_DIR :str = "artifacts"
FILE_NAME :str = "SmartETA.csv"

TRAIN_FILE_NAME :str = "train.csv"
TEST_FILE_NAME :str = "test.csv"

SCHEMA_FILE_PATH = os.path.join("data_schema", "schema.yaml")


"""
Data Ingestion related constants starts with DATA_INGESTION
"""

DATA_INGESTION_DIR_NAME :str = "data_ingestion"
DATA_INGESTION_COLLECTION_NAME :str = "eta_data"
DATA_INGESTION_DATABASE_NAME :str = "smarteta"
DATA_INGESTION_FEATURE_STORE_DIR :str = "feature_store"
DATA_INGESTION_INGESTED_DIR: str = "ingested"
DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO : float = 0.2

"""
Data Validation related constants starts with DATA_VALIDATION
"""
DATA_VALIDATION_DIR_NAME :str = "data_validation"
DATA_VALIDATION_VALID_DIR : str = "valid"
DATA_VALIDATION_INVALID_DIR : str = "invalid"
DATA_VALIDATION_DRIFT_REPORT_DIR : str = "drift_report"
DATA_VALIDATION_DRIFT_REPORT_FILE_NAME : str = "report.yaml"
