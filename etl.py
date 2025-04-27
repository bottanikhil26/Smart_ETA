
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import os
import sys
import json
import certifi
import pandas as pd
import numpy as np
from src.smarteta.exception.exception import SmartetaException
from src.smarteta.logging.logger import logging


from dotenv import load_dotenv
load_dotenv()

MONGO_DB_URL =os.getenv("MONGO_DB_URL")
ca = certifi.where() #Certifi Authority (Trusted)


class ETL():
    def _init__(self):
        try:
            pass
        except Exception as e:
            raise SmartetaException(e, sys) from e
        
    def cvs_to_json_conertor(self,file_path):
        try:
            data = pd.read_csv(file_path)
            data.reset_index(drop=True,inplace=True)
            records = list(json.loads(data.T.to_json()).values())
            return records

        except Exception as e:
            raise SmartetaException(e, sys) from e
    
    def insert_data_to_mongodb(self,records,database,collection):
        try:
            self.database = database
            self.collection = collection
            self.records = records
            self.client = MongoClient(MONGO_DB_URL, server_api=ServerApi('1'),tlsCAFile=ca)
            self.database = self.client[self.database]
            self.collection = self.database[self.collection]
            self.collection.insert_many(self.records)  
            logging.info(f"Data inserted successfully to {self.database} database and {self.collection} collection")
            return (len(self.records))
        except Exception as e:
            raise SmartetaException(e, sys) from e




if __name__ == "__main__":
    etl = ETL()
    file_path = "Data/train.csv"
    records = etl.cvs_to_json_conertor(file_path)
    print(f"Converted {len(records)} records to JSON format.")
    database = "smarteta"
    collection = "eta_data"
    inserted_count = etl.insert_data_to_mongodb(records, database, collection)
    print(f"Inserted {inserted_count} records into MongoDB.")





