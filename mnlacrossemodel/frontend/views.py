from datetime import datetime
from dateutil import parser
from mnlacrossemodel.backend.model import Model

import pandas as pd
from django.shortcuts import render


def create_upcoming_games_table():
    # get all games in this upcoming season's schedule that are today and tomorrow
    data = pd.read_csv('mnlacrossemodel/backend/data/team_data/2020-complete-schedule/2020-schedule.csv', index_col=[0])

    games_today_and_tomorrow = []
    for row in data.itertuples():
        string_date = getattr(row, 'date')

        game_date = parser.parse(string_date)
        curr_date = datetime.now()

        time_difference = game_date - curr_date

        if time_difference.days < 25:
            games_today_and_tomorrow.append([
                getattr(row, 'home_team'),
                getattr(row, 'away_team'),
                getattr(row, 'date')
            ])

    return games_today_and_tomorrow


def index(request):
    """
    Controller for index page.
    :param request: http request
    :return: index page view
    """
    model = Model()
    upcoming_games = create_upcoming_games_table()

    upcoming_games_with_prediction = []
    for upcoming_game in upcoming_games:
        home_team = upcoming_game[0]
        away_team = upcoming_game[1]
        pred_score = model.predict_score(home_team, away_team)
        if pred_score is not None:
            upcoming_games_with_prediction.append([home_team, pred_score.get('Home'), away_team, pred_score.get('Away')])

    context = {
        'upcoming_games': upcoming_games_with_prediction
    }

    return render(request, 'index.html', context)
