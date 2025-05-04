import sys
import os
from datetime import datetime
import pandas as pd
import numpy as np
import holidays
import pickle
from geopy.distance import geodesic
import datetime
from datetime import timedelta
from sklearn.preprocessing import LabelEncoder, OrdinalEncoder
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.cluster import MiniBatchKMeans
from src.smarteta.constants import TARGET_COLUMN_NAME , FINAL_VARIABLES, label_encoding, ordinal_cols, Road_traffic_density_order, City_order
from src.smarteta.exception.exception import SmartetaException
from src.smarteta.logging.logger import logging
from src.smarteta.config.configuration import DataTransformationConfig
from src.smarteta.entity.artifact_entity import DataTransformationArtifact, DataValidationArtifact

from src.smarteta.utils.common import  save_dataframe, save_object



class DataTransformation:
    def __init__(self,data_validation_artifact: DataValidationArtifact,
                 data_transformation_config: DataTransformationConfig):
        try:
            self.data_validation_artifact : DataValidationArtifact = data_validation_artifact
            self.data_transformation_config : DataTransformationConfig = data_transformation_config
        except Exception as e:
            raise SmartetaException(e, sys) from e
        
    
    @staticmethod    
    def read_data(file_path) -> pd.DataFrame:
        """
        This function reads the data from a csv file.
        """
        try:
            data = pd.read_csv(file_path)
            return data
        except Exception as e:
            raise SmartetaException(e, sys) from e
    @staticmethod   
    def distance(lat1,lon1,lat2,lon2):
        try:
            """
            This function calculates the distance between two points on the earth.
            """
            # Calculate the distance
            return geodesic((lat1,lon1),(lat2,lon2)).km
        except Exception as e:
            raise SmartetaException(e, sys) from e
        
    def converting_dtypes(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        This function converts dtypes in correct form.
        """
        try:
        
            data["Weatherconditions"] = data["Weatherconditions"].str.split(" ").str[-1]
            data['Delivery_person_Age']=pd.to_numeric(data['Delivery_person_Age'] ,errors ='coerce')
            data['Delivery_person_Ratings'] = pd.to_numeric(data['Delivery_person_Ratings'],errors = 'coerce')
            data['Order_Date'] = pd.to_datetime(data['Order_Date'])
            data['multiple_deliveries'] = pd.to_numeric(data['multiple_deliveries'])
            data['Time_taken(min)'] = data["Time_taken(min)"].str.extract(r"(\d+)").astype("Int64")

            return data
        except Exception as e:
            raise SmartetaException(e, sys) from e
        
    def feature_generation(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        This function performs feature generation on the data.
        """
        try:
            data=data.drop(data[(data["Restaurant_latitude"]==0.00) & (data['Restaurant_longitude']==0.00)].index)
            #calculating distance 
            data['distance'] = data.apply(lambda x: self.distance(x['Restaurant_latitude'],x['Restaurant_longitude'],x['Delivery_location_latitude'],x['Delivery_location_longitude']),axis=1)
            data = data[data['distance']< 20]
            data['City_Name'] = data['Delivery_person_ID'].str.extract(r'^(.*?)RES')
            data['month'] = data['Order_Date'].dt.month
            data['day_of_week'] = data['Order_Date'].dt.dayofweek
            data['weekend'] = data['day_of_week'].apply(lambda x: 1 if x in [5,6] else 0)
            data['day'] = data['Order_Date'].dt.day
            data['quarter'] = data['Order_Date'].dt.quarter
            data['Ordered_time'] = pd.to_datetime(data['Order_Date'].astype(str)+' '+data['Time_Orderd'].astype(str), errors='coerce')
            data['Picked_with_time'] = pd.to_datetime(data['Order_Date'].astype(str) + ' ' + data['Time_Order_picked'].astype(str), errors='coerce')
            mask = data['Picked_with_time'] < data['Ordered_time']
            data.loc[mask, 'Picked_with_time'] += timedelta(days=1)
            data['Food_preparation_time'] = (data['Picked_with_time'] - data['Ordered_time']).dt.total_seconds() / 60
            coords = np.vstack((data[['Restaurant_latitude', 'Restaurant_longitude']].values,
                                data[['Delivery_location_latitude', 'Delivery_location_longitude']].values))
            sample_ind = np.random.permutation(len(coords))
            kmeans = MiniBatchKMeans(n_clusters=22, batch_size=10000).fit(coords[sample_ind])
            data.loc[:, 'pickup_cluster'] = kmeans.predict(data[['Restaurant_latitude', 'Restaurant_longitude']])
            data.loc[:, 'dropoff_cluster'] = kmeans.predict(data[['Delivery_location_latitude', 'Delivery_location_longitude']])
            return data
        except Exception as e:
            raise SmartetaException(e, sys) from e
        
    def missing_value_imputation(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        This function performs missing value imputation on the data.
        """
        try:
            #Numeric columns
            data['Delivery_person_Age'] = data['Delivery_person_Age'].fillna(
                data.groupby(['Delivery_person_ID','City'])['Delivery_person_Age'].transform('mean'))

            data['Delivery_person_Age'] = data['Delivery_person_Age'].fillna(data.groupby(['Delivery_person_ID'])['Delivery_person_Age'].transform('mean'))

            data['Delivery_person_Ratings'] = data['Delivery_person_Ratings'].fillna(
                data.groupby(['Delivery_person_ID'])['Delivery_person_Ratings'].transform('mean'))

            data['multiple_deliveries'] = data['multiple_deliveries'].fillna(data['multiple_deliveries'].median())
            data['Food_preparation_time']=data['Food_preparation_time'].fillna(data.groupby(['City_Name'])['Food_preparation_time'].transform('median'))

            #Categorical columns
            data['Road_traffic_density'] = data['Road_traffic_density'].fillna('Missing')
            data['Weatherconditions'] = data['Weatherconditions'].fillna('Missing')
            data['City'] = data['City'].fillna('Missing')
            indian_holidays = holidays.India(years=2022)
            data['Festival'] = data['Festival'].fillna(
                data.apply(lambda x: 'Yes' if pd.isna(x['Festival']) and x['Order_Date'] in indian_holidays else 'No', axis=1))
            return data
        except Exception as e:
            raise SmartetaException(e, sys) from e
        
    def encoding(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        This function performs encoding on the data.
        """
        try:
            # Label Encoding
            label_encoder = LabelEncoder()
            for column in label_encoding:
                data[column] = label_encoder.fit_transform(data[column])
            # Ordinal Encoding
            ordinal_encoder = OrdinalEncoder(categories=[Road_traffic_density_order, City_order])
            data[ordinal_cols] = ordinal_encoder.fit_transform(data[ordinal_cols])
            return data
        except Exception as e:
            raise SmartetaException(e, sys) from e
    
    def final_transformation(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        This function performs final transformation on the data.
        """
        try:
            data = data[FINAL_VARIABLES]
            return data
        except Exception as e:
            raise SmartetaException(e, sys) from e


    def initiate_data_transformation(self)-> DataTransformationArtifact:
        """
        This function initiates the data transformation process.
        """
        try:
            logging.info("Data Transformation process started")
            # Load the data
            train_df = DataTransformation.read_data(self.data_validation_artifact.valid_train_file_path)
            test_df =  DataTransformation.read_data(self.data_validation_artifact.valid_test_file_path)
            logging.info("Data loaded successfully")
            # Convert dtypes
            train_df = self.converting_dtypes(train_df)
            test_df = self.converting_dtypes(test_df)
            logging.info("Data types converted successfully")
        

            target_feature_train_df = train_df[TARGET_COLUMN_NAME]
            target_feature_test_df = test_df[TARGET_COLUMN_NAME]

            train_df.drop(columns=[TARGET_COLUMN_NAME], inplace=True)
            test_df.drop(columns=[TARGET_COLUMN_NAME], inplace=True)

            # Feature generation
            train_df = self.feature_generation(train_df)
            test_df = self.feature_generation(test_df)
            logging.info("Feature generation completed successfully")
            # missing value imputation
            train_df = self.missing_value_imputation(train_df)
            test_df = self.missing_value_imputation(test_df)
            logging.info("Missing value imputation completed successfully")
            # Encoding
            train_df = self.encoding(train_df)
            test_df = self.encoding(test_df)
            logging.info("Encoding completed successfully")
            # Final transformation
            train_df = self.final_transformation(train_df)
            test_df = self.final_transformation(test_df)
            logging.info("Final transformation completed successfully")

            # concat the train and train target
            train_df = pd.concat([train_df, target_feature_train_df], axis=1)
            test_df = pd.concat([test_df, target_feature_test_df], axis=1)

            
# Save the transformed data
            save_dataframe(self.data_transformation_config.transformed_train_file_path, train_df)
            save_dataframe(self.data_transformation_config.transformed_test_file_path, test_df)
            logging.info("Transformed data saved successfully")

            data_transformation_artifact = DataTransformationArtifact(
                transformed_train_file_path=self.data_transformation_config.transformed_train_file_path,
                transformed_test_file_path=self.data_transformation_config.transformed_test_file_path
            )

            logging.info("Data Transformation process completed successfully")
            return data_transformation_artifact
        except Exception as e:
            raise SmartetaException(e, sys) from e

