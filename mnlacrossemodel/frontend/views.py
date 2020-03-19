from datetime import datetime, timedelta
from dateutil import parser

import pandas as pd
from django.http import HttpResponse


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

    print(create_upcoming_games_table())

    text = """
    <h3>Welcome.</h3>
    <table width="50%" border="1">
    <tr>
        <td>aaa</td>
        <td>bbb</td>
    </tr>
    <tr>
        <td>ccc</td>
        <td>ddd</td>
    </tr>
    </table>
    """
    return HttpResponse(text)
