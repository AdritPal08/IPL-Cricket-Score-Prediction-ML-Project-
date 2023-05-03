import pandas as pd
import sys
from dataclasses import dataclass
from exception import CustomException
from logger import logging
import datetime
import os
@dataclass
class DATA_EDAConfig:
    match_data_path: str=os.path.join('artifacts',"match_data.csv")
    match_info_path: str=os.path.join('artifacts',"match_info.csv")
class DATA_EDA:
    def __init__(self):
        self.eda_config=DATA_EDAConfig()
    def data_eda(self,df,df_info):
        try:
            logging.info("The exploratory data analysis (EDA) process has been initiated")
            logging.info("1. Replacing old boling and batting team name with current name")
            # define a dictionary to map the values to be replaced with their corresponding replacements
            replace_dict = {'Delhi Daredevils': 'Delhi Capitals','Deccan Chargers':'Sunrisers Hyderabad','Pune Warriors':'Rising Pune Supergiants','Rising Pune Supergiant':'Rising Pune Supergiants','Gujarat Lions':'Gujarat Titans','Kings XI Punjab':'Punjab Kings'}
            ## Match Dataset
            df['batting_team'].replace(replace_dict,inplace=True)
            df['bowling_team'].replace(replace_dict,inplace=True)
            ## Match info
            df_info['team1'].replace(replace_dict,inplace=True)
            df_info['team2'].replace(replace_dict,inplace=True)
            df_info['toss_winner'].replace(replace_dict,inplace=True)
            df_info['winner'].replace(replace_dict,inplace=True)
            ## Creating a column of the short name of all the teams
            # Define the mapping dictionary
            logging.info("2. Create a short name column of batting and bowling teams")
            short_name = {'Kolkata Knight Riders': 'KKR',
                        'Royal Challengers Bangalore':'RCB',
                        'Chennai Super Kings':'CSK',
                        'Punjab Kings':'PBKS',
                        'Rajasthan Royals':'RR',
                        'Delhi Capitals':'DC',
                        'Sunrisers Hyderabad':'SRH',
                        'Mumbai Indians':'MI',
                        'Kochi Tuskers Kerala':'KTK',
                        'Rising Pune Supergiants':'RPSG',
                        'Gujarat Titans':'GT',
                        'Lucknow Super Giants':'LSG'}
            # Map the values of batting_team column to shortnames
            df['batting_team_short_name'] = df['batting_team'].map(short_name)

            # Map the values of bowling_team column to shortnames
            df['bowling_team_short_name'] = df['bowling_team'].map(short_name)
            
            logging.info("3. Renaming column name")
            ## Renaming column name
            # Match Dataset
            # Rename column 'venue' to 'Stadium'
            df = df.rename(columns={'venue': 'stadium'})
            # Rename column 'ball' to 'over'
            df = df.rename(columns={'ball': 'over'})
            # Match info
            # Rename column 'venue' to 'Stadium'
            df_info = df_info.rename(columns={'venue': 'stadium'})
            
            logging.info("4. Create a 'venue' column to include the venue information for each stadium")
            ## Create a 'venue' column to include the venue information for each stadium
            venue_stadium = {'M Chinnaswamy Stadium':'Bengaluru',
         'Punjab Cricket Association Stadium, Mohali':'Mohali',
         'Feroz Shah Kotla':'Delhi',
         'Eden Gardens': 'Kolkata',
         'Wankhede Stadium' : 'Mumbai',
         'Sawai Mansingh Stadium': 'Jaipur',
         'Rajiv Gandhi International Stadium, Uppal':'Hyderabad',
         'MA Chidambaram Stadium, Chepauk': 'Chennai',
         'Dr DY Patil Sports Academy' : 'Mumbai',
         'Newlands': 'Cape Town, South Africa',
         "St George's Park" : 'Gqeberha, South Africa',
        'Kingsmead' : 'Durban, KwaZulu-Natal, South Africa',
        'SuperSport Park' : 'Centurion, South Africa',
         'Buffalo Park': 'East London, Eastern Cape, South Africa',
          'New Wanderers Stadium':'Johannesburg, South Africa',
         'De Beers Diamond Oval' : 'Kimberley, South Africa',
         'OUTsurance Oval': 'Bloemfontein, South Africa',
         'Brabourne Stadium':'Mumbai',
         'Brabourne Stadium, Mumbai':'Mumbai',
         'Sardar Patel Stadium, Motera':'Ahmedabad',
         'Barabati Stadium':'Cuttack',
         'Vidarbha Cricket Association Stadium, Jamtha':'Jamtha',
         'Himachal Pradesh Cricket Association Stadium' :'Dharamshala',
         'Nehru Stadium':'Delhi',
         'Holkar Cricket Stadium': 'Indore',
         'Dr. Y.S. Rajasekhara Reddy ACA-VDCA Cricket Stadium' :'Visakhapatnam',
         'Subrata Roy Sahara Stadium' : 'Pune',
         'Maharashtra Cricket Association Stadium': 'Pune',
         'Maharashtra Cricket Association Stadium' : 'Pune',
         'Shaheed Veer Narayan Singh International Stadium': 'Raipur',
         'JSCA International Stadium Complex': 'Ranchi',
         'Sheikh Zayed Stadium' :'Abu Dhabi, UAE',
         'Sharjah Cricket Stadium' :'Sharjah, UAE',
         'Dubai International Cricket Stadium' : 'Dubai, UAE',
         'Punjab Cricket Association IS Bindra Stadium, Mohali' : 'Mohali',
         'Saurashtra Cricket Association Stadium': 'Rajkot',
         'Green Park' :'Kanpur',
         'M.Chinnaswamy Stadium' : 'Bengaluru',
         'MA Chidambaram Stadium': 'Chennai',
         'Arun Jaitley Stadium' : 'Delhi',
         'Rajiv Gandhi International Stadium':'Hyderabad',
         'Punjab Cricket Association IS Bindra Stadium': 'Mohali',
         'MA Chidambaram Stadium, Chepauk, Chennai': 'Chennai',
         'Wankhede Stadium, Mumbai': 'Mumbai',
         'Narendra Modi Stadium, Ahmedabad':'Ahmedabad',
         'Arun Jaitley Stadium, Delhi':'Delhi', 
         'Zayed Cricket Stadium, Abu Dhabi' : 'Abu Dhabi, UAE',
         'Dr DY Patil Sports Academy, Mumbai' : 'Mumbai',
         'Maharashtra Cricket Association Stadium, Pune' : 'Pune',
         'Eden Gardens, Kolkata': 'Kolkata'
        }
            # Match Datset
            # Map the values of stadium column to venue_stadium
            df['venue'] = df['stadium'].map(venue_stadium)

            # Match info
            # Map the values of stadium column to venue_stadium
            df_info['venue'] = df_info['stadium'].map(venue_stadium)
            
            logging.info("5. Create a 'actual_name_stadium' column to include the actual name of each stadium")
            ##Create a 'actual_name_stadium' column to include the actual name of each stadium
            actual_name_stadium = {'Brabourne Stadium': 'Brabourne Stadium, Mumbai',
                'M Chinnaswamy Stadium' : 'Mangalam Chinnaswamy Stadium',
                'Punjab Cricket Association Stadium, Mohali':'Inderjit Singh Bindra Stadium',
                'Feroz Shah Kotla':'Arun Jaitley Cricket Stadium',
                'Eden Gardens' :'Eden Gardens',
                'Wankhede Stadium' : 'Sheshrao Krushnarao Wankhede Stadium',
                'Sawai Mansingh Stadium' :'Sawai Mansingh Stadium',
                'Rajiv Gandhi International Stadium, Uppal' :'Rajiv Gandhi International Stadium',
                'MA Chidambaram Stadium, Chepauk': 'M.A. Chidambaram stadium',
                'Dr DY Patil Sports Academy' : 'Dr. D.Y. Patil Sports Academy',
                'Newlands' :'Newlands',
                "St George's Park": "St George's Park",
                'Kingsmead':'Kingsmead',
                'SuperSport Park':'SuperSport Park',
                'Buffalo Park':'Buffalo Park',
                'New Wanderers Stadium':'New Wanderers Stadium',
                'De Beers Diamond Oval':'De Beers Diamond Oval',
                'Sardar Patel Stadium, Motera':'Narendra Modi Stadium',
                'Barabati Stadium':'Barabati Stadium',
                'Vidarbha Cricket Association Stadium, Jamtha': 'Vidarbha Cricket Association Jamtha Stadium',
                'Himachal Pradesh Cricket Association Stadium':'Himachal Pradesh Cricket Association Stadium',
                'Nehru Stadium':'Jawaharlal Nehru University Stadium',
                'Holkar Cricket Stadium':'Holkar Cricket Stadium',
                'Dr. Y.S. Rajasekhara Reddy ACA-VDCA Cricket Stadium' : 'Dr. Y.S. Rajasekhara Reddy ACA-VDCA Cricket Stadium',
                'Subrata Roy Sahara Stadium' : 'Maharashtra Cricket Association Stadium',
                'Maharashtra Cricket Association Stadium' :'Maharashtra Cricket Association Stadium',
                'Maharashtra Cricket Association Stadium' :'Maharashtra Cricket Association Stadium',
                'Shaheed Veer Narayan Singh International Stadium': 'Shaheed Veer Narayan Singh International Cricket Stadium',
                'JSCA International Stadium Complex' : 'Jharkhand State Cricket Association International Cricket Stadium',
                'Sheikh Zayed Stadium':'Sheikh Zayed Cricket Stadium',
                'Sharjah Cricket Stadium' : 'Sharjah Cricket Stadium',
                'Dubai International Cricket Stadium' : 'Dubai International Cricket Stadium',
                'Punjab Cricket Association IS Bindra Stadium, Mohali': 'Inderjit Singh Bindra Stadium',
                'Saurashtra Cricket Association Stadium': 'Khandheri Cricket Stadium',
                'Green Park' : 'Green Park Cricket Stadium',
                'M.Chinnaswamy Stadium' : 'Mangalam Chinnaswamy Stadium',
                'MA Chidambaram Stadium': 'M.A. Chidambaram stadium',
                'Arun Jaitley Stadium': 'Arun Jaitley Cricket Stadium',
                'Rajiv Gandhi International Stadium':'Rajiv Gandhi International Stadium',
                'Punjab Cricket Association IS Bindra Stadium': 'Inderjit Singh Bindra Stadium',
                'MA Chidambaram Stadium, Chepauk, Chennai': 'M.A. Chidambaram stadium',
                'Wankhede Stadium, Mumbai': 'Sheshrao Krushnarao Wankhede Stadium',
                'Narendra Modi Stadium, Ahmedabad':'Narendra Modi Stadium',
                'Arun Jaitley Stadium, Delhi' : 'Arun Jaitley Cricket Stadium',
                'Zayed Cricket Stadium, Abu Dhabi' : 'Sheikh Zayed Cricket Stadium',
                'Dr DY Patil Sports Academy, Mumbai' : 'Dr. D.Y. Patil Sports Academy',
                'Maharashtra Cricket Association Stadium, Pune' :'Maharashtra Cricket Association Stadium',
                'Eden Gardens, Kolkata': 'Eden Gardens',
                'OUTsurance Oval': 'Mangaung Oval',
                'Brabourne Stadium, Mumbai':'Brabourne Stadium, Mumbai'
               }
            # Match Dataset
            # Map the values of stadium column to actual_name_stadium
            df['actual_name_stadium'] = df['stadium'].map(actual_name_stadium)

            # Match info
            # Map the values of stadium column to actual_name_stadium
            df_info['actual_name_stadium'] = df_info['stadium'].map(actual_name_stadium)
            
            logging.info("6. Converting the column 'date' from string into datetime object")
            ##Converting the column 'date' from string into datetime object
            
            ## Match Dataset
            # Converting the column 'date' from string into datetime object
            df['start_date'] = df['start_date'].apply(lambda x: datetime.datetime.strptime(x, '%Y-%m-%d'))

            ## Match info
            # Converting the column 'date' from string into datetime object
            df_info['date'] = df_info['date'].apply(lambda x: datetime.datetime.strptime(x, '%Y-%m-%d'))
            
            logging.info("7. Creating a column of 'total_run' to calculate total run")
            ## creating a column of 'total_run' to calculate total run
            #calculate total_run
            df['total_run'] = df['runs_off_bat'] +df['extras']
            
            logging.info("8. Creating a column of final_total_runs")
            ##Creating a column of final_total_runs
            #create a new column called final_total_runs
            df['final_total_runs'] = 0

            # group by match_id and innings, and sum the total runs
            total_runs = df.groupby(['match_id', 'innings'])['total_run'].sum().reset_index()

            # loop through each row in total_runs
            for i, row in total_runs.iterrows():
                # find the corresponding rows in the main dataframe and update the final_total_runs column
                df.loc[(df['match_id'] == row['match_id']) & (df['innings'] == row['innings']), 'final_total_runs'] = row['total_run']
                
            logging.info("9. Create a new column 'is_wicket' based on 'wicket_type'")
            ##Create a new column "is_wicket" based on "wicket_type"
            # Create a new column "is_wicket" based on "wicket_type"
            df['is_wicket'] = df['wicket_type'].apply(lambda x: 1 if pd.notnull(x) and x != '' else 0)
            
            logging.info("10. Creating column 'wickets' and 'runs' to calculate total runs and wickets till particular over")
            ## Creating column 'wickets' and 'runs' to calculate total runs and wickets till particular over
            # Let's group the dataframe by match_id and innings
            grouped = df.groupby(["match_id", "innings"])

            # Let's calculate the cumulative sum of wickets, runs, and balls
            df["wickets"] = grouped["is_wicket"].cumsum()
            df["runs"] = grouped["total_run"].cumsum()            
            
            df = df[['match_id', 'season', 'start_date', 'stadium', 'actual_name_stadium', 'venue', 'innings', 'over',
         'batting_team', 'batting_team_short_name', 'bowling_team', 'bowling_team_short_name', 'striker', 'non_striker', 'bowler',
         'runs_off_bat', 'extras', 'total_run', 'final_total_runs', 'runs', 'wides', 'noballs', 'byes', 'legbyes',
         'penalty', 'wicket_type', 'is_wicket', 'wickets', 'player_dismissed', 'other_wicket_type',
         'other_player_dismissed']]
            df_info = df_info[['match_id', 'season', 'date', 'city', 'stadium','actual_name_stadium','venue', 'team1', 'team2',
       'toss_winner', 'toss_decision', 'player_of_match', 'winner',
       'winner_wickets', 'winner_runs', 'outcome', 'result_type', 'results',
       'gender', 'event', 'match_number', 'umpire1', 'umpire2',
       'reserve_umpire', 'tv_umpire', 'match_referee', 'eliminator', 'method',
       'date_1']]
            
            logging.info("11. Save all the Datset")
            ##save dataset
            os.makedirs(os.path.dirname(self.eda_config.match_data_path),exist_ok=True)

            df.to_csv(self.eda_config.match_data_path,index=False,header=True)
            
            os.makedirs(os.path.dirname(self.eda_config.match_info_path),exist_ok=True)

            df_info.to_csv(self.eda_config.match_info_path,index=False,header=True)
            
            logging.info("The exploratory data analysis (EDA) process has been completed")
            return (self.eda_config.match_data_path)
        except Exception as e:
            raise CustomException(e,sys)