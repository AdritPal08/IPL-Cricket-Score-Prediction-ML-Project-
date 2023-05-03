from utils import LoadArtifacts
from exception import CustomException
from logger import logging
import sys
from flask import Flask, request, render_template

app = Flask(__name__)
teams, venues = LoadArtifacts.load_artifacts()

teams.sort()
venues.sort()

@app.route("/")
def home():
    return render_template("home.html", team = teams, venue = venues)

@app.route("/predictedScore", methods = ["POST"])
def predicted_score():
    try:
        venue = request.form["venue"]
        bat_team = request.form["bat_team"]
        bowl_team = request.form["bowl_team"]
        overs = float(request.form["overs"])
        runs = int(request.form["runs"])
        wickets = int(request.form["wickets"])
        innings = int(request.form["innings"])

        result = int(LoadArtifacts.predict_score(bat_team,bowl_team,innings,overs,runs,wickets,venue))
        
        if result == 1:
            return "Something is wrong please fill proper input!!"
        else:
            return "Predicted score range of " + bat_team + " is between " + str(result - 5) + " to " + str(result + 5)
    except Exception as e:
            raise CustomException(e, sys)

if __name__ == "__main__":
    app.run()
