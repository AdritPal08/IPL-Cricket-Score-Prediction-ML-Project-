import numpy as np
import pickle
import json
from exception import CustomException
from logger import logging
import sys
from dataclasses import dataclass
import os


model = None
scaler = None
columns = None
encoded_teams = None

@dataclass
class LoadArtifacts:
    
    def load_artifacts():
        global model
        global scaler
        global columns
        global encoded_teams

        with open(os.path.join(os.getcwd(), "artifacts/model.pickle"), "rb") as f:
            model = pickle.load(f)

        with open(os.path.join(os.getcwd(), "artifacts/scaler.pickle"), "rb") as f:
            scaler = pickle.load(f)

        with open(os.path.join(os.getcwd(), "artifacts/columns.json"), "r") as f:
            columns = np.array(json.load(f)["columns"])

        with open(os.path.join(os.getcwd(), "artifacts/encodedteams.json"), "r") as f:
            encoded_teams = json.load(f)

        return list(encoded_teams.keys()), columns[6:].tolist()

    # def predict_score(self, batting_team, bowling_team, innings, over, runs, wickets, venue, columns):
    def predict_score(batting_team:str, bowling_team:str, innings:int, over:int, runs:int, wickets:int, venue:str):
        
        try:
            X_pred = np.zeros(columns.size)

            X_pred[0:2] = [encoded_teams[batting_team], encoded_teams[bowling_team]]
            

            X_pred[2:6] = [innings, over, runs, wickets]


            if venue != "Abu Dhabi, UAE":
                venue_index = np.where(columns == venue)[0][0]  # add 1 to skip the first column
                X_pred[venue_index] = 1

            # Set the feature names of the input data
            # scaler.feature_names = columns.tolist()
            # scaler.set_params(feature_names=columns.tolist())
            # Scale the input data
            X_pred = scaler.transform([X_pred])

            result = model.predict(X_pred)[0]
            result = int(result)
            return result
        except Exception as e:
            raise CustomException(e, sys)

# if __name__ == "__main__":
#     load = LoadArtifacts()
#     teams, venues = load.load_artifacts()
#     result = load.predict_score("Royal Challengers Bangalore", "Delhi Capitals", 2, 8, 96, 1, "Bengaluru")
#     # result = round(result, 2)
#     # result = int(result)
#     print(result)
