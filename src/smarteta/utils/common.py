import yaml
from src.smarteta.exception.exception import SmartetaException
from src.smarteta.logging.logger import logging
import os 
import sys
import pandas as pd
import numpy as pd
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