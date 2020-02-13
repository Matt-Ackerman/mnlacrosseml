import pandas as pd

from datetime import datetime


def create_mock_data():
    """
    Used for testing while waiting for the upcoming season schedule to be released.
    :return: mock data representing future games
    """
    mock_data = [
        ['Minnetonka', 'Farmington', 'Mock date'],
        ['Lakeville North', 'Shakopee', 'Mock date']
    ]
    df = pd.DataFrame(mock_data, columns=[
        'home_team',
        'away_team',
        'date'
    ])


if __name__ == "__main__":
    create_mock_data()
    a = 'a'