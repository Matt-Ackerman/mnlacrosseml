import os
from datetime import datetime

import pandas as pd
import requests
from dateutil import parser
from bs4 import BeautifulSoup
from mnlacrossemodel.backend.model import Model


class PredictionRunner:

    def __init__(self):
        self.model = Model()
        self.BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    # def create_upcoming_game_predictions(self):
    #     data = pd.read_csv(self.BASE_DIR + '/backend/data/team_data/2020-complete-schedule/2020-schedule.csv', index_col=[0])
    #     games_today_and_tomorrow = []
    #     for row in data.itertuples():
    #         string_date = getattr(row, 'date')
    #
    #         game_date = parser.parse(string_date)
    #         curr_date = datetime.now()
    #
    #         time_difference = game_date - curr_date
    #
    #         if 0 <= time_difference.days < 20:
    #             games_today_and_tomorrow.append([
    #                 getattr(row, 'home_team'),
    #                 getattr(row, 'away_team'),
    #                 getattr(row, 'date')
    #             ])
    #
    #     upcoming_games_with_prediction = []
    #     for upcoming_game in games_today_and_tomorrow:
    #         home_team = upcoming_game[0]
    #         away_team = upcoming_game[1]
    #         date = upcoming_game[2]
    #         pred_score = self.model.predict_score(home_team, away_team)
    #
    #         if pred_score is not None:
    #             upcoming_games_with_prediction.append([home_team, pred_score.get('Home'), away_team, pred_score.get('Away'), date])
    #
    #     df = pd.DataFrame(upcoming_games_with_prediction, columns=[
    #         'home_team',
    #         'home_team_pred_score',
    #         'away_team',
    #         'away_team_pred_score',
    #         'date'
    #     ])
    #     print('--- updating the upcoming predictions csv')
    #     df.to_csv(self.BASE_DIR + '/backend/data/prediction_data/upcoming-predictions.csv')

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

            if -50 <= time_difference.days < 0:
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

        # append past games instead of replacing
        df.to_csv(self.BASE_DIR + '/backend/data/prediction_data/past-predictions.csv', mode='a', header=False)





    def create_upcoming_gameday_predictions(self, month, day):
        url = "https://www.mnlaxhub.com/schedule/day/league_instance/114505?subseason=672672"
        gameday = self.get_games_from_gameday(url)

        date = gameday[0]
        games_table = gameday[1]

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
        df.to_csv(self.BASE_DIR + '/backend/data/prediction_data/upcoming-predictions.csv')
        print('--- updated the upcoming predictions csv')




    def create_past_game_predictions(self, month, day):
        # games = get_game_tables_for_date()

        game_results = []
        # loop through each game result in the table
        for game in games:
            game_data = []
            for column in game.find_all('td'):
                column_value = column.text.replace("'", "").replace("/", " ").replace("\n", "").lstrip().rstrip()
                game_data.append(column_value)

            game_data = game_data[0:4]
            game_data.append(month + '/' + day)
            game_results.append(game_data)

        a = 1

    def get_games_from_gameday(self, url):

        # date_slider_page = "https://www.mnlaxhub.com/schedule/day/league_instance/114505/2020/" + month + "/" + day + "?subseason=672672"

        page = requests.get("https://www.mnlaxhub.com/schedule/day/league_instance/114505/2020/4/13?subseason=672672&referrer=5590472")
        soup = BeautifulSoup(page.content, 'html.parser')

        table = soup.find('table', class_='statTable sortable noSortImages')
        games = table.find_all('tr', class_='odd scheduled compactGameList')
        games = games + table.find_all('tr', class_='even scheduled compactGameList')
        date = soup.find('div', class_='pageElement').text.replace("\n", "").lstrip().rstrip()
        return [date, games]

    def get_games_from_gameday(self, url):

        # date_slider_page = "https://www.mnlaxhub.com/schedule/day/league_instance/114505/2020/" + month + "/" + day + "?subseason=672672"

        page = requests.get("https://www.mnlaxhub.com/schedule/day/league_instance/114505/2020/4/13?subseason=672672&referrer=5590472")
        soup = BeautifulSoup(page.content, 'html.parser')

        table = soup.find('table', class_='statTable sortable noSortImages')
        games = table.find_all('tr', class_='odd completed compactGameList')
        games = games + table.find_all('tr', class_='even completed compactGameList')
        date = soup.find('div', class_='pageElement').text.replace("\n", "").lstrip().rstrip()
        return [date, games]


if __name__ == "__main__":
    p = PredictionRunner()
    p.create_upcoming_gameday_predictions('4', '9')



    a = 1
