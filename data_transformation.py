import sys
from dataclasses import dataclass
from exception import CustomException
from logger import logging
import os
import pickle
import json
import pandas as pd
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.model_selection import train_test_split

@dataclass
class Data_transformation_config:
    scaler_path: str = os.path.join('artifacts',"scaler.pickle")
    encoded_teams_path: str = os.path.join('artifacts',"encodedteams.json")
    columns_path: str = os.path.join('artifacts',"columns.json")
    X_data_path: str = os.path.join('artifacts',"X.csv")
    Y_data_path: str = os.path.join('artifacts',"Y.csv")
class Data_transformation:
    def __init__(self):
        self.transformation_config=Data_transformation_config()
        
    def initiate_data_transformation(self,math_data_path):
        try:
            logging.info("Data Transformation process has been initiated")
            df=pd.read_csv(math_data_path,low_memory=False)
            
            ## Feature Selection and Removing unwanted columns
            # Removing unwanted columns and rearranging columns
            logging.info("1. Removing unwanted columns and rearranging columns")
            columns_to_remove = ['match_id', 'season', 'striker', 'non_striker', 'bowler',
                     'runs_off_bat', 'extras', 'wides', 'noballs', 'byes', 'legbyes',
                     'penalty', 'wicket_type', 'player_dismissed', 'other_wicket_type',
                     'other_player_dismissed', 'batting_team_short_name','start_date',
                     'bowling_team_short_name', 'total_run', 'is_wicket', 'stadium', 'actual_name_stadium']

            df1 = df.drop(columns=columns_to_remove)[["batting_team", "bowling_team", "venue",
                                          "innings", "over", "runs", "wickets", "final_total_runs"]]
            logging.info("2. Feature Encoding")
            ## Feature Encoding
            encoded_teams = {k:v for v, k in enumerate(pd.concat([df1['batting_team'], df1['bowling_team']]).unique(), 0)}
            df1['batting_team'] = df1['batting_team'].map(encoded_teams)
            df1['bowling_team'] = df1['bowling_team'].map(encoded_teams)
            
            logging.info("3. Preparing X and Y variables")
            ## Preparing X and Y variables
            X =df1.drop(columns=['final_total_runs'],axis=1)
            Y = df1['final_total_runs']
            Y = pd.DataFrame(Y)
            
            logging.info("4. Instantiate OneHotEncoding")
            ## OneHotEncoding
            # Get the column names of numerical and categorical features
            num_features = X.select_dtypes(exclude="object").columns
            cat_features = X.select_dtypes(include="object").columns

            # Instantiate OneHotEncoder
            encoder = OneHotEncoder()

            # Use fit_transform() to encode the specified columns
            encoded_features = encoder.fit_transform(X[cat_features])

            # The encoded_features will be in a sparse matrix format, you can convert it to a dense array using toarray()
            # If you want to append it to the original dataframe, you can convert it to a dataframe using pd.DataFrame()
            encoded_features_df = pd.DataFrame(encoded_features.toarray(), columns=encoder.get_feature_names_out(cat_features))

            # Remove the "venue_" prefix from column names in the encoded features dataframe
            encoded_features_df.columns = [col.split("venue_")[1] for col in encoded_features_df.columns]

            # Concatenate the encoded features dataframe with the original dataframe
            X = pd.concat([X.drop(cat_features, axis=1), encoded_features_df], axis=1)
            
            
            logging.info("5. Save all the files")   
            os.makedirs(os.path.dirname(self.transformation_config.encoded_teams_path),exist_ok=True)
            with open(self.transformation_config.encoded_teams_path,"w") as path2:
                json.dump(encoded_teams,path2)
                
            os.makedirs(os.path.dirname(self.transformation_config.columns_path),exist_ok=True)
            with open(self.transformation_config.columns_path,"w") as path3:
                json.dump({"columns": list(X.columns)},path3)
                
            os.makedirs(os.path.dirname(self.transformation_config.X_data_path),exist_ok=True)
            X.to_csv(self.transformation_config.X_data_path,index=False,header=True)
            
            os.makedirs(os.path.dirname(self.transformation_config.Y_data_path),exist_ok=True)
            Y.to_csv(self.transformation_config.Y_data_path,index=False,header=True)
            
            
            return(self.transformation_config.X_data_path,self.transformation_config.Y_data_path)
        except Exception as e:
            raise CustomException(e,sys)
            
    def train_test_split(self,X,Y) :
        try:
            logging.info("6. Separate dataset into train and test")   
            ## Separate dataset into train and test
            X_train, X_test, Y_train, Y_test = train_test_split(X,Y,test_size=0.2,random_state=42)
            
            logging.info("7. Scaling the dataset") 
            ## Scaling the dataset
            scaler = StandardScaler()
            X_train = scaler.fit_transform(X_train)
            X_test = scaler.transform(X_test)
            
            logging.info("8. Save scaler files")
            ## saving files
            os.makedirs(os.path.dirname(self.transformation_config.scaler_path),exist_ok=True)
            with open(self.transformation_config.scaler_path,"wb") as path:
                pickle.dump(scaler,path)
                
            logging.info("Data Transformation process has been completed")
            return (X_train, X_test, Y_train, Y_test)
        
        except Exception as e:
            raise CustomException(e,sys)