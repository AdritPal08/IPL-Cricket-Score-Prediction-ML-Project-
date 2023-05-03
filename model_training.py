import sys
from dataclasses import dataclass
from exception import CustomException
from logger import logging
from data_transformation import Data_transformation
import os
import pandas as pd
import numpy as np
import pickle
from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error
from sklearn.model_selection import GridSearchCV, RandomizedSearchCV
from sklearn.ensemble import RandomForestRegressor, AdaBoostRegressor, GradientBoostingRegressor
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from typing import Tuple

@dataclass
class ModelTraining_config:
    model_path: str = os.path.join('artifacts',"model.pickle")
    best_model_details_path: str = os.path.join('artifacts',"best_model_details.csv")
class ModelTraining:
    def __init__(self):
        self.model_config=ModelTraining_config()
        
    def evaluate_model(self, true: np.ndarray, predicted: np.ndarray) -> Tuple[float, float, float, float]:
    
        try:
            mae = mean_absolute_error(true, predicted)
            mse = mean_squared_error(true, predicted)
            rmse = np.sqrt(mse)
            r2_square = r2_score(true, predicted)
            return mae, mse, rmse, r2_square
        except Exception as e:
            raise CustomException(e, sys)
    
    def model_training(self, X_path: str, Y_path: str) -> Tuple[dict, pd.DataFrame, pd.DataFrame] :
        try:
            X =pd.read_csv(X_path)
            Y =pd.read_csv(Y_path)
            # X_train, X_test, Y_train, Y_test = train_test_split(X,Y,test_size=0.2,random_state=42)
            ## Scaing the dataset
            # scaler = StandardScaler()
            # X_train = scaler.fit_transform(X_train)
            # X_test = scaler.transform(X_test)
            train_test_split = Data_transformation()
            X_train, X_test, Y_train, Y_test = train_test_split.train_test_split(X,Y)
            logging.info("Model Training process has been initiated")
            algos = {
    "Linear Regression": {
        "model": LinearRegression(),
        "params": {}
    },
    "Ridge": {
        "model": Ridge(),
        "params": {
            "alpha":np.arange(0.1, 1, 0.01)
        }
    },
    "Lasso": {
        "model": Lasso(),
        "params": {
            "alpha": np.arange(0.1, 1, 0.01)
        }
    },
    
}

            
            train_model_error = []
            test_model_error = []
            best_model_details = []
            final_model = {}
            logging.info("1. Train and evaluate models")
            # Train and evaluate models
            for model_name, values in algos.items():
                
                grid_search = GridSearchCV(values["model"], values["params"], scoring='neg_mean_squared_error', cv=5)
                # grid_search = RandomizedSearchCV(values["model"], values["params"], cv=5, n_iter=15, n_jobs=-1, verbose=2, random_state=4)
                grid_search.fit(X_train, Y_train)
                best_score = grid_search.best_score_
                best_params = grid_search.best_params_
                
                best_model_details.append({"Model Name": model_name, "Best Score": best_score, "Best Parameters": best_params})
                # Fit model with best hyperparameters
                best_model = values["model"].set_params(**best_params)
                best_model.fit(X_train, Y_train)
                final_model[model_name] = best_model
                # Make predictions
                Y_train_pred = best_model.predict(X_train)
                Y_test_pred = best_model.predict(X_test)
                
                # Evaluate Train and Test dataset
                model_train_mae , model_train_mse, model_train_rmse, model_train_r2 = self.evaluate_model(Y_train, Y_train_pred)
                model_test_mae , model_test_mse, model_test_rmse, model_test_r2 = self.evaluate_model(Y_test, Y_test_pred)
                
                train_model_error.append({"Model Name": model_name, "Mean Absolute Error": model_train_mae, "Mean Squared Error": model_train_mse, "Root Mean Squared Error": model_train_rmse,"r2 score":model_train_r2})
                test_model_error.append({"Model Name": model_name, "Mean Absolute Error": model_test_mae, "Mean Squared Error": model_test_mse, "Root Mean Squared Error": model_test_rmse,"r2 score":model_test_r2})
               
                
            best_model_details = pd.DataFrame(best_model_details)
                
            ## Chosing the best model
            # Compare train and test data errors for each model
            train_model_error = pd.DataFrame(train_model_error)
            test_model_error = pd.DataFrame(test_model_error)
            
            logging.info("2. Compare train and test data errors and Choose the best-performing model")
            # Choose the best-performing model based on evaluation metrics
            best_model = None
            # Find the model with the lowest MAE
            best_mae = min(test_model_error['Mean Absolute Error'])
            best_models_mae = test_model_error[test_model_error['Mean Absolute Error'] == best_mae]['Model Name'].values
            best_model = ', '.join(best_models_mae)

            # Find the model with the lowest MSE
            best_mse = min(test_model_error['Mean Squared Error'])
            best_models_mse = test_model_error[test_model_error['Mean Squared Error'] == best_mse]['Model Name'].values
            best_model += ', ' + ', '.join([model for model in best_models_mse if model not in best_models_mae])

            # Find the model with the lowest RMSE
            best_rmse = min(test_model_error['Root Mean Squared Error'])
            best_models_rmse = test_model_error[test_model_error['Root Mean Squared Error'] == best_rmse]['Model Name'].values
            best_model += ', ' + ', '.join([model for model in best_models_rmse if model not in best_models_mae and model not in best_models_mse])

            # Find the model with the highest R2 score
            best_r2 = max(test_model_error['r2 score'])
            best_models_r2 = test_model_error[test_model_error['r2 score'] == best_r2]['Model Name'].values
            best_model += ', ' + ', '.join([model for model in best_models_r2 if model not in best_models_mae and model not in best_models_mse and model not in best_models_rmse])
            save_model=best_model.split(",")[0]
            logging.info(f"Best Model is: {save_model}")
                
            logging.info("3. Saving all files")    
            ## saving
            logging.info("Saving best model details") 
            os.makedirs(os.path.dirname(self.model_config.best_model_details_path),exist_ok=True)
            best_model_details.to_csv(self.model_config.best_model_details_path,index=False,header=True)
            
            logging.info("Saving the best model with params")     
            os.makedirs(os.path.dirname(self.model_config.model_path),exist_ok=True)
            with open(self.model_config.model_path,"wb") as path:
                pickle.dump(final_model[save_model],path)
                
            logging.info("Model Training process has been completed")    
            return(final_model[save_model] )    
              
        except Exception as e:
            raise CustomException(e,sys)