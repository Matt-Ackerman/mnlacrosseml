import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

from sklearn.linear_model import LogisticRegression, LinearRegression

from mnlacrossemodel.backend.data.data_prep import get_team_profile_stats


def test_out_models():
    # load
    data = pd.read_csv('/Users/matt/Desktop/mn-lacrosse-ml/ml/growing-ml-dataset.csv', index_col=[0])

    # split and drop unwanted values
    x = data.drop(['home_team', 'home_team_score', 'away_team', 'away_team_score', 'winner', 'year'], axis=1)
    y = data.winner

    # train and test split data
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)

    # applying standard scaling to get optimized result
    # sc = StandardScaler()
    # x_train - sc.fit_transform(x_train)
    # x_test = sc.transform(x_test)

    # random forest classifier performs relatively poorly

    # try out naive bayes?


def logistic_regression_win_model():
    """

    :return:
    """
    # load
    data = pd.read_csv('/Users/matt/Desktop/mn-lacrosse-ml/ml/growing-ml-dataset.csv', index_col=[0])

    # split and drop unwanted values
    x = data.drop(['home_team', 'home_team_score', 'away_team', 'away_team_score', 'winner', 'year'], axis=1)
    y = data.winner

    # train and test split data
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)

    # Create instance (i.e. object) of LogisticRegression
    logmodel = LogisticRegression()
    logmodel.fit(x_train, y_train)
    predictions = logmodel.predict(x_test)

    # lets see how rfc does
    print(classification_report(y_test, predictions))

    return logmodel


def multivariate_linear_regression_score_model():
    """
    multivariate linear regression
    :return:
    """
    # load
    data = pd.read_csv('/Users/matt/Desktop/mn-lacrosse-ml/ml/growing-ml-dataset.csv', index_col=[0])

    # split and drop unwanted values
    x = data.drop(['home_team', 'home_team_score', 'away_team', 'away_team_score', 'winner', 'year'], axis=1)
    y = data.drop(['home_team_record', 'home_team_GFvGA', 'away_team_record', 'away_team_GFvGA', 'home_team', 'away_team', 'winner', 'year'], axis=1)

    # train and test split data
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)

    # Create instance (i.e. object) of LogisticRegression
    linmodel = LinearRegression()
    linmodel.fit(x_train, y_train)

    return linmodel


def create_game_for_prediction(home_team_name, away_team_name):
    # 1. find the profile of both team_data
    home_team = get_team_profile_stats(home_team_name)
    away_team = get_team_profile_stats(away_team_name)

    # 2. create a record for the game that mirrors those in our model_data-dataset.csv
    game_to_predict = [
        home_team.Record,
        home_team.GFvGA,
        away_team.Record,
        away_team.GFvGA,
    ]

    return game_to_predict


    # def create_past_game_predictions(self):
    #     """
    #     Moves games from upcoming to past.
    #     """
    #     data = pd.read_csv(self.BASE_DIR + '/backend/data/prediction_data/live-predictions.csv')
    #     past_games_with_predictions = []
    #     for row in data.itertuples():
    #         string_date = getattr(row, 'date')
    #
    #         game_date = parser.parse(string_date)
    #         curr_date = datetime.now()
    #
    #         time_difference = game_date - curr_date
    #
    #         if -50 <= time_difference.days < 0:
    #             past_games_with_predictions.append([
    #                 getattr(row, 'home_team'),
    #                 getattr(row, 'home_team_pred_score'),
    #                 getattr(row, 'away_team'),
    #                 getattr(row, 'away_team_pred_score'),
    #                 getattr(row, 'date')
    #             ])
    #
    #     df = pd.DataFrame(past_games_with_predictions, columns=[
    #         'home_team',
    #         'home_team_pred_score',
    #         'away_team',
    #         'away_team_pred_score',
    #         'date'
    #     ])
    #
    #     print('--- updating the past predictions csv')
    #
    #     # append past games instead of replacing
    #     df.to_csv(self.BASE_DIR + '/backend/data/prediction_data/prediction-results.csv', mode='a', header=False)


if __name__ == "__main__":
    # create models
    win_model = logistic_regression_win_model()
    score_model = multivariate_linear_regression_score_model()

    # create record for game we want to predict
    game_to_predict = create_game_for_prediction('Minnetonka', 'Lakeville South')

    # predict it
    pred_result = score_model.predict([game_to_predict])

    print('-----')
    print(pred_result)
