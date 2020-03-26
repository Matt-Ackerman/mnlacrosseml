import os
import pandas as pd
from django.shortcuts import render

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def index(request):
    """
    Controller for index page.
    :param request: http request
    :return: render for the index page view
    """

    live_predictions = get_live_predictions_table_records()
    prediction_results = get_results_table_records()

    context = {
        'live_predictions': live_predictions,
        'prediction_results': prediction_results
    }

    return render(request, 'index.html', context)


def get_live_predictions_table_records():
    """
    1. Returns the records from the live-predictions.csv file.
    """

    live_predictions_df = pd.read_csv(BASE_DIR + '/backend/data/prediction_data/live-predictions.csv', index_col=[0])
    games = live_predictions_df.values

    live_predictions = []
    for game in games:
        live_predictions.append([game[0], game[1], game[2], game[3], game[4]])

    return live_predictions


def get_results_table_records():
    """
    1. Returns the records from the prediction-results.csv file.
    """

    prediction_results_df = pd.read_csv(BASE_DIR + '/backend/data/prediction_data/prediction-results.csv', index_col=[0])
    games = prediction_results_df.values

    prediction_results = []
    for game in games:
        prediction_results.append([game[0], game[1], game[2], game[3], game[4]])

    return prediction_results
