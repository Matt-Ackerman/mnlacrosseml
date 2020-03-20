import os
import pandas as pd
from django.shortcuts import render

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def index(request):
    """
    Controller for index page.
    :param request: http request
    :return: index page view
    """
    upcoming_game_predictions = get_upcoming_game_predictions()
    past_game_predictions = get_past_game_predictions()
    context = {
        'upcoming_game_predictions': upcoming_game_predictions,
        'past_game_predictions': past_game_predictions
    }

    return render(request, 'index.html', context)


def get_upcoming_game_predictions():
    upcoming_games_dataframe = pd.read_csv(BASE_DIR + '/backend/data/prediction_data/upcoming-predictions.csv', index_col=[0])
    games = upcoming_games_dataframe.values

    upcoming_game_predictions = []
    for game in games:
        upcoming_game_predictions.append([game[0], game[1], game[2], game[3], game[4]])

    return upcoming_game_predictions


def get_past_game_predictions():
    past_games_dataframe = pd.read_csv(BASE_DIR + '/backend/data/prediction_data/past-predictions.csv', index_col=[0])
    games = past_games_dataframe.values

    past_game_predictions = []
    for game in games:
        past_game_predictions.append([game[0], game[1], game[2], game[3], game[4]])

    return past_game_predictions