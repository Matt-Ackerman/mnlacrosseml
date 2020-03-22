import os
import requests
import pandas as pd
from dateutil import parser
from bs4 import BeautifulSoup
from mnlacrossemodel.backend.model import Model


class PredictionRunner:

    def __init__(self):
        self.model = Model()
        self.BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    def create_upcoming_gameday_predictions(self):
        url = "https://www.mnlaxhub.com/schedule/day/league_instance/114505?subseason=672672"
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')

        table = soup.find('table', class_='statTable sortable noSortImages')
        games = table.find_all('tr', class_='odd scheduled compactGameList')
        games_table = games + table.find_all('tr', class_='even scheduled compactGameList')
        date = soup.find('div', class_='pageElement').text.replace("\n", "").lstrip().rstrip()

        # loop through each game in the gameday table
        upcoming_games = []
        for game in games_table:
            game_data = []
            for column in game.find_all('td'):
                column_value = column.text.replace("'", "").replace("/", " ").replace("\n", "").lstrip().rstrip()
                if column_value is not '-':
                    game_data.append(column_value)

            game_data = game_data[0:2]
            game_data.append(date)
            upcoming_games.append(game_data)

        # add model prediction to each game
        upcoming_games_with_prediction = []
        for game in upcoming_games:
            home_team = game[1]
            away_team = game[0]
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
        df.to_csv(self.BASE_DIR + '/backend/data/prediction_data/live-predictions.csv')
        print('--- updated the live predictions')

    def create_past_game_predictions(self):
        # checking what date our upcoming predictions are on
        prediction_data = pd.read_csv(self.BASE_DIR + '/backend/data/prediction_data/live-predictions.csv')
        string_date = prediction_data.loc[0,'date']
        date = parser.parse(string_date)

        # go to the url that shows the actual results for the games we predicted
        url = "https://www.mnlaxhub.com/schedule/day/league_instance/114505/2020/" + str(date.month) + "/" + str(date.day) + "?subseason=672672"
        page = requests.get(url)
        if page.status_code is 200:
            soup = BeautifulSoup(page.content, 'html.parser')

            table = soup.find('table', class_='statTable sortable noSortImages')
            games = table.find_all('tr', class_='odd completed compactGameList')
            games = games + table.find_all('tr', class_='even completed compactGameList')

            # loop through each game's actual results in the table
            game_results = []
            for game in games:
                game_data = []
                for column in game.find_all('td'):
                    column_value = column.text.replace("'", "").replace("/", " ").replace("\n", "").lstrip().rstrip()
                    game_data.append(column_value)

                game_data = game_data[0:4]
                game_results.append(game_data)


            # find the game predictions records and match/combine them with our actual results
            combined_pred_and_actual = []
            for prediction in prediction_data.itertuples():
                home_team = getattr(prediction, 'home_team')
                away_team = getattr(prediction, 'away_team')
                for result in game_results:
                    if home_team == result[0] and away_team == result[2]:
                        date = getattr(prediction, 'date')
                        home_team_pred_score = getattr(prediction, 'home_team_pred_score')
                        away_team_pred_score = getattr(prediction, 'away_team_pred_score')
                        combined_pred_and_actual.append([home_team, result[1], away_team, result[3], date, home_team_pred_score, away_team_pred_score])

            df = pd.DataFrame(combined_pred_and_actual, columns=[
                'home_team',
                'home_team_actual_score',
                'away_team',
                'away_team_actual_score',
                'date',
                'home_team_pred_score',
                'away_team_pred_score',
            ])


            # append past games instead of replacing
            df.to_csv(self.BASE_DIR + '/backend/data/prediction_data/prediction-results.csv', mode='a', header=False)
            print('--- updated the prediction results')


if __name__ == "__main__":
    p = PredictionRunner()
    p.create_past_game_predictions()
    a = 1
