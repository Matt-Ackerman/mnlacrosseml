import os
from datetime import datetime

import pandas as pd
from dateutil import parser
from mnlacrossemodel.backend.model import Model


class PredictionRunner:

    def __init__(self):
        self.model = Model()
        self.BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    def create_upcoming_game_predictions(self):
        data = pd.read_csv(self.BASE_DIR + '/backend/data/team_data/2020-complete-schedule/2020-schedule.csv', index_col=[0])
        games_today_and_tomorrow = []
        for row in data.itertuples():
            string_date = getattr(row, 'date')

            game_date = parser.parse(string_date)
            curr_date = datetime.now()

            time_difference = game_date - curr_date

            if time_difference.days < 20:
                games_today_and_tomorrow.append([
                    getattr(row, 'home_team'),
                    getattr(row, 'away_team'),
                    getattr(row, 'date')
                ])

        upcoming_games_with_prediction = []
        for upcoming_game in games_today_and_tomorrow:
            home_team = upcoming_game[0]
            away_team = upcoming_game[1]
            date = upcoming_game[2]
            pred_score = self.model.predict_score(home_team, away_team)

            if pred_score is not None:
                upcoming_games_with_prediction.append([home_team, pred_score.get('Home'), away_team, pred_score.get('Away'), date])

        df = pd.DataFrame(upcoming_games_with_prediction, columns=[
            'home_team',
            'home_team_pred_score',
            'away_team',
            'away_team_pred_score',
            'date'
        ])
        print('--- updating the upcoming predictions csv')
        df.to_csv(self.BASE_DIR + '/backend/data/prediction_data/upcoming-predictions.csv')

    def create_past_game_predictions(self):
        """
        Moves games from upcoming to past.
        """
        data = pd.read_csv(self.BASE_DIR + '/backend/data/prediction_data/upcoming-predictions.csv')
        past_games_with_predictions = []
        for row in data.itertuples():
            string_date = getattr(row, 'date')

            game_date = parser.parse(string_date)
            curr_date = datetime.now()

            time_difference = game_date - curr_date

            if time_difference.days < 0:
                past_games_with_predictions.append([
                    getattr(row, 'home_team'),
                    getattr(row, 'home_team_pred_score'),
                    getattr(row, 'away_team'),
                    getattr(row, 'away_team_pred_score'),
                    getattr(row, 'date')
                ])

        df = pd.DataFrame(past_games_with_predictions, columns=[
            'home_team',
            'home_team_pred_score',
            'away_team',
            'away_team_pred_score',
            'date'
        ])

        print('--- updating the past predictions csv')

        # TODO: append past games instead of replacing
        df.to_csv(self.BASE_DIR + '/backend/data/prediction_data/past-predictions.csv')