import os

import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from mnlacrossemodel.backend.data.data_prep import get_team_profile_stats


class Model:

    def __init__(self):
        self.linear_regression = self.create_multivariate_lin_reg_score_model()

    def predict_score(self, home_team, away_team):
        game_to_predict = self.create_game_for_prediction(home_team, away_team)

        if game_to_predict is None:
            return None

        predicted_result = self.linear_regression.predict([game_to_predict])

        pred_home_score = predicted_result[0][0]
        pred_away_score = predicted_result[0][1]
        # fix decimals and ties
        rounded_home_score = int(round(pred_home_score))
        rounded_away_score = int(round(pred_away_score))
        if rounded_home_score == rounded_away_score:
            if pred_home_score < pred_away_score:
                rounded_away_score += 1
            else:
                rounded_home_score += 1

        return {'Home': rounded_home_score, 'Away': rounded_away_score}

    def create_game_for_prediction(self, home_team_name, away_team_name):
        # 1. find the profile of both team_data
        home_team = get_team_profile_stats(home_team_name)
        away_team = get_team_profile_stats(away_team_name)

        # 2. create a record for the game that mirrors those in our model_data-dataset.csv

        if home_team is None or away_team is None:
            return None

        game_to_predict = [
            home_team.Record,
            home_team.GFvGA,
            away_team.Record,
            away_team.GFvGA,
        ]

        return game_to_predict

    def create_multivariate_lin_reg_score_model(self):
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        data = pd.read_csv(BASE_DIR + '/backend/data/model_data/ml-dataset.csv', index_col=[0])

        # split and drop unwanted values
        x = data.drop([
            'home_team',
            'home_team_score',
            'away_team',
            'away_team_score',
            'winner',
            'year',
            'date'
        ], axis=1)
        y = data.drop([
            'home_team_record',
            'home_team_GFvGA',
            'away_team_record',
            'away_team_GFvGA',
            'home_team',
            'away_team',
            'winner',
            'year',
            'date'
        ], axis=1)

        # train and test split data
        x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)

        # Create instance (i.e. object) of LogisticRegression
        linmodel = LinearRegression()
        linmodel.fit(x_train, y_train)

        return linmodel