import os
import sys
from exception import CustomException
from logger import logging
import pandas as pd

from dataclasses import dataclass
from data_EDA import DATA_EDA
from data_transformation import Data_transformation
from model_training import ModelTraining

@dataclass

class DataIngestion:
    
    def initiate_data_ingestion(self):
        logging.info("Data Ingestion process has been initiated")
        try:
            df=pd.read_csv('notebook\data\ipl_match_ball_by_ball_data.csv',low_memory=False) ## Match Dataset
            df_info =pd.read_csv('notebook\data\ipl_match_info_data.csv',low_memory=False)   ## Match info
            logging.info("Successfully load all the datasets")
            logging.info("Data Ingestion process has been completed")
            return(df,df_info)
        except Exception as e:
            raise CustomException(e,sys)
        
if __name__=="__main__":
    obj=DataIngestion()
    df,df_info=obj.initiate_data_ingestion()
    
    eda=DATA_EDA()
    math_data_path=eda.data_eda(df,df_info)
    
    transformation = Data_transformation()
    X_path, Y_path = transformation.initiate_data_transformation(math_data_path=math_data_path)

    # print(X.head(5))
    # print(Y.head(5))
    
    
    
    # model_training= ModelTraining()
    # model_training.model_training(X,Y)
    model_training_= ModelTraining()
    model_training_.model_training(X_path,Y_path)
    
    