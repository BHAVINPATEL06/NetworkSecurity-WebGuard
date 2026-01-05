## Here we import DataIngestionArtifact and DataValidationConfig classes from the entity module,
## As the DataIngestionArtifact class output will be the input for DataValidation component.

## Here we import SCHEMA_FILE_PATH constant for data validation purpose.
## Basically to check whether the dataset columns and data types are as per the schema defined in the schema.yaml file.

from networksecurity.entity.artifact_entity import DataIngestionArtifact,DataValidationArtifact
from networksecurity.entity.config_entity import DataValidationConfig
from networksecurity.constant.training_pipeline import SCHEMA_FILE_PATH
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
from networksecurity.utils.main_utils.utils import read_yaml_file,write_yaml_file

## For data drifting detection we are using the evidently library.
from scipy.stats import ks_2samp
import pandas as pd
import os, sys


class DataValidation:
## Here we constructed a constructor of DataValidation class which will
##  accept two arguments DataIngestionArtifact as input  and DataValidationConfig objects as output
    def __init__(self,data_ingestion_artifact:DataIngestionArtifact,
                data_validation_config:DataValidationConfig):
        try:
            self.data_ingestion_artifact = data_ingestion_artifact
            self.data_validation_config = data_validation_config
            self.schema_config = read_yaml_file(SCHEMA_FILE_PATH)
        except Exception as e:
            raise NetworkSecurityException(e,sys)

## Here we are reading the data from the file path using pandas library
## staticmethod is a decorator that defines a method that does not operate on an instance of the class
    @staticmethod
    def read_data(file_path)->pd.DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        

## Here we are validating the no of columns in the dataset is as per the schema defined in the schema.yaml file.
    def validate_number_of_columns(self,dataframe:pd.DataFrame)->bool:
        try:
            number_of_columns = len(self.schema_config)
            logging.info(f"Required number of columns: {number_of_columns}")
            logging.info(f"Dataframe has columns: {len(dataframe.columns)}")
            if len(dataframe.columns) == number_of_columns:
                return True
            return False
        except Exception as e:
            raise NetworkSecurityException(e,sys)


    def numerical_columns_exist(self,dataframe:pd.DataFrame)->bool:
        try:
            numerical_columns = self.schema_config['numerical_columns']
            dataframe_columns = dataframe.columns
            missing_numerical_columns = []
            for num_column in numerical_columns:
                if num_column not in dataframe_columns:
                    missing_numerical_columns.append(num_column)
            if len(missing_numerical_columns)>0:
                logging.info(f"Missing numerical columns: {missing_numerical_columns}")
                return False
            return True
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def detect_data_drift(self,base_df,current_df,threshold = 0.05)->bool:
        try:
            status = True
            report = {}
            for column in base_df.columns:
                d1 = base_df[column]
                d2 = current_df[column]
                is_same_dist = ks_2samp(d1,d2)

                if threshold<=is_same_dist.pvalue:
                    isFound = False
                else:
                    isFound = True
                    status = False
                report.update({column:{
                    "p_value":float(is_same_dist.pvalue),
                    "drift_status":isFound 
                }})
            drift_report_file_path = self.data_validation_config.drift_report_file_path

            ## Creating directory
            dir_path= os.path.dirname(drift_report_file_path)
            os.makedirs(dir_path,exist_ok=True)
            write_yaml_file(file_path=drift_report_file_path,content=report)

        except Exception as e:
            raise NetworkSecurityException(e,sys)

## Here we are initiating the data validation method which will have return type of  DataValidationArtifact object
    def initiate_data_validation(self)->DataValidationArtifact:
        try:
            ## Getting train and test file path from data ingestion artifact
            train_file_path = self.data_ingestion_artifact.trained_file_path
            test_file_path = self.data_ingestion_artifact.test_file_path

            ## Reading the train and test file 
            train_dataframe = DataValidation.read_data(train_file_path)
            test_dataframe = DataValidation.read_data(test_file_path)

            ## Validating number of columns
            status = self.validate_number_of_columns(dataframe=train_dataframe)
            if not status:
                error_message = f"Train dataframe does not contain all columns \n"
            
            status = self.validate_number_of_columns(dataframe=test_dataframe)
            if not status:
                error_message = f"Test dataframe does not contain all columns \n"

            ## Let's check Data Drift
            status = self.detect_data_drift(base_df=train_dataframe,current_df=test_dataframe)
            dir_path = os.path.dirname(self.data_validation_config.valid_train_file_path)
            os.makedirs(dir_path,exist_ok=True)

            train_dataframe.to_csv(self.data_validation_config.valid_train_file_path,index=False,header=True)
            test_dataframe.to_csv(self.data_validation_config.valid_test_file_path,index=False,header=True)

            ## returning the DataValidationArtifact object
            data_validation_artifact = DataValidationArtifact(
                validation_status = status,
                valid_train_file_path = self.data_ingestion_artifact.trained_file_path,
                valid_test_file_path = self.data_ingestion_artifact.trained_file_path,
                invalid_train_file_path = None,
                invalid_test_file_path = None,
                drift_report_file_path = self.data_validation_config.drift_report_file_path
            )
            return data_validation_artifact
        
        except Exception as e:
            raise NetworkSecurityException(e,sys)
