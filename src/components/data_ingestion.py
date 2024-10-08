import os
import sys
from src.exception import CustomException  # first we import exception 
from src.logger import logging   #noe remove the logging term

import pandas as pd
from sklearn.model_selection import train_test_split # need of train_test_split 

from dataclasses import dataclass

from src.components.data_transformation import DataTransformation
from src.components.data_transformation import DataTransformationConfig

from src.components.model_trainer import ModelTrainerConfig
from src.components.model_trainer import ModelTrainer

@dataclass #decorator
class DataIngestionConfig:
    # to save the test train test the data in artifacts and with this csv files name
    train_data_path: str=os.path.join('artifacts',"train.csv")  
    test_data_path: str=os.path.join('artifacts',"test.csv")
    raw_data_path: str=os.path.join('artifacts',"data.csv")


class DataIngestion:
    def __init__(self): 
        self.ingestion_config=DataIngestionConfig() #ingestion_config  this consist of above all three data part


# initiate_data_ingestion -- if data stored in some databases then write the code over here to read in the database
# i can create mongodb or sql client in util.py i can read it
 
    def initiate_data_ingestion(self):
        logging.info("Entered the data ingestion method or component")
        try:
            df=pd.read_csv('notebook\data\stud.csv')
            logging.info('Read the dataset as dataframe')

            os.makedirs(os.path.dirname(self.ingestion_config.train_data_path),exist_ok=True)

            df.to_csv(self.ingestion_config.raw_data_path,index=False,header=True)

            logging.info("Train test split initiated")
            train_set,test_set=train_test_split(df,test_size=0.2,random_state=42)

            train_set.to_csv(self.ingestion_config.train_data_path,index=False,header=True)

            test_set.to_csv(self.ingestion_config.test_data_path,index=False,header=True)

            logging.info("Inmgestion of the data iss completed")

            return(
                self.ingestion_config.train_data_path,
                self.ingestion_config.test_data_path

            )
        except Exception as e:
            raise CustomException(e,sys)
        
if __name__=="__main__":
    obj=DataIngestion()
    train_data,test_data=obj.initiate_data_ingestion()

    data_transformation=DataTransformation()
    train_arr,test_arr,_r=data_transformation.initiate_data_transformation(train_data,test_data) # we will make var train test data after pkl file generated during the data transformation 

    modeltrainer=ModelTrainer()
    print(modeltrainer.initiate_model_trainer(train_arr,test_arr))



