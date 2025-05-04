import yaml
from src.smarteta.exception.exception import SmartetaException
from src.smarteta.logging.logger import logging
import os 
import sys
import pandas as pd
import numpy as np
#import dill
import pickle


def read_yaml_file(file_path : str) -> dict:
    try:
        with open(file_path, 'rb') as file:
            return yaml.safe_load(file)
    except Exception as e:
        raise SmartetaException(e, sys) from e
    
def write_yaml_file(file_path : str, content: object ,replace : bool = False) -> None:
    try:
        """
        This function writes the content to a yaml file.
        """
        if replace:
            if os.path.exists(file_path):
                os.remove(file_path)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'w') as file:
            yaml.dump(content, file)
    except Exception as e:
        raise SmartetaException(e, sys) from e
    

def save_dataframe(file_path: str, df: pd.DataFrame) -> None:
    try:
        """
        This function saves a pandas DataFrame to a CSV file.
        """
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        df.to_csv(file_path, index=False)
    except Exception as e:
        raise SmartetaException(e, sys) from e
    
def save_object(file_path: str, obj: object) -> None:
    try:
        """
        This function saves an object to a file.
        """
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'wb') as file:
            pickle.dump(obj, file)
    except Exception as e:
        raise SmartetaException(e, sys) from e