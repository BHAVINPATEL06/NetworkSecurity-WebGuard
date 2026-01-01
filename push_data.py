### THiS SCRIPT IS AN ETL PIPELINE (EXTRACT TRANSFORM LOAD)
### THIS SCRIPT EXTRACTS THE DATA FROM CSV FILE, TRANSFORMS IT TO JSON RECORDS
### AND LOADS IT TO MONGODB ATLAS DATABASE

import os
import sys
import json

## This is used to load the environment variables from .env file
from dotenv import load_dotenv
load_dotenv()

MONGO_DB_URL = os.getenv("MONGO_DB_URL")
print(MONGO_DB_URL)

## This is used to handle the certified HTTPS connections over MONGODB Atlas
import certifi
## This ca is required to provide the certificate authority file for secure connection
ca = certifi.where()

import pandas as pd
import numpy as np
import pymongo
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging


## This class is used to extract the data from CSV file and push it to MongoDB Atlas
class NetworkDataExtract():

## This is the constructor of the class
    def __init__(self):
        try:
            pass
        except Exception as e:
            raise NetworkSecurityException(e, sys)

## This function is used to convert the CSV file to JSON records
    def csv_to_json(self,file_path):
        try:
            data = pd.read_csv(file_path)
            data.reset_index(drop=True, inplace=True)  ## Remove the default index column
            records=list(json.loads(data.T.to_json()).values()) ## Convert the dataframe to json records
            return records
        except Exception as e:
            raise NetworkSecurityException(e, sys)

## This function is used to insert the data to MongoDB Atlas
    def insert_data_to_mongoDB(self,records,database,collection):
        try:
            self.database = database
            self.collection = collection
            self.records = records

            self.mongo_client = pymongo.MongoClient(MONGO_DB_URL)
            self.database = self.mongo_client[self.database]
            self.collection = self.database[self.collection]
            self.collection.insert_many(self.records)
            return (len(self.records))

        except Exception as e:
            raise NetworkSecurityException(e, sys)


if __name__ == "__main__":
    FILE_PATH = 'Network_Data/phishingData.csv'
    DATABASE = 'BhavinDB'
    Collection = 'NetworkData'
    network_obj = NetworkDataExtract()
    records = network_obj.csv_to_json(file_path=FILE_PATH)
    print(records)
    no_of_records = network_obj.insert_data_to_mongoDB(records,DATABASE,Collection)
    print(f"No of records inserted to MongoDB Atlas: {no_of_records}")

