import os
import pandas as pd


def create_team_profiles():
    """
    Creates a profile csv with overall stats for each team that we have created a schedule team-schedule-results csv for.
    """
    root_dir = '/Users/matt/Desktop/mnlacrossemodel/mnlacrossemodel/backend/data'
    schedule_directory = root_dir + '/team_data/team-schedule-results/'
    # loop through schedule team-schedule-results for each team in a given year
    for filename in os.listdir(schedule_directory):
        if filename.endswith("-results.csv"):
            df = pd.read_csv(schedule_directory + filename)

            # capture record
            results = df['Result'].sum()
            wins = results.count('W')
            losses = results.count('L')
            record = wins / (wins + losses)

            # capture goals for vs goals against
            goals_for = df['Goals For'].sum()
            goals_against = df['Goals Against'].sum()
            for_vs_against = goals_for / (goals_for + goals_against)

            # create file for team profile
            df2 = pd.DataFrame([[str(record), str(for_vs_against)]], columns=['Record', 'GFvGA'])
            df2.to_csv(root_dir + '/team_data/team-profiles/' + filename[0:filename.index('~')] + '~profile.csv')


def create_records_for_ml_dataset():
    """
    Creates the full list of game records with the accompanying team profile stats that we will run machine learning on.
    :return:
    """
    game_records = []

    root_dir = '/Users/matt/Desktop/mnlacrossemodel/mnlacrossemodel/backend/data'
    schedule_directory = root_dir + '/team_data/team-schedule-results/'
    # loop through schedule team-schedule-results for each team
    for filename in os.listdir(schedule_directory):
        if filename.endswith("-results.csv"):
            df = pd.read_csv(schedule_directory + filename)
            for row in df.iterrows():
                game = row[1]
                if game.Location == 'Home':
                    home_team = filename[0:filename.index('~')]
                    away_team = game['Opponent']
                    home_team_score = game['Goals For']
                    away_team_score = game['Goals Against']
                    if game.Result == 'W':
                        winner = 0
                    else:
                        winner = 1
                else:
                    home_team = game['Opponent']
                    away_team = filename[0:filename.index('~')]
                    home_team_score = game['Goals Against']
                    away_team_score = game['Goals For']
                    if game.Result == 'W':
                        winner = 1
                    else:
                        winner = 0

                # get home and away team team-profiles
                home_team_profile = get_team_profile_stats(home_team)
                away_team_profile = get_team_profile_stats(away_team)

                if home_team_profile is not None and away_team_profile is not None:
                    home_team_record = home_team_profile.Record
                    home_team_GFvGA = home_team_profile.GFvGA

                    away_team_record = away_team_profile.Record
                    away_team_GFvGA = away_team_profile.GFvGA

                    game_record = [
                        home_team,
                        home_team_score,
                        home_team_record,
                        home_team_GFvGA,
                        away_team,
                        away_team_score,
                        away_team_record,
                        away_team_GFvGA,
                        winner,
                        game.Year,
                        game.Date
                    ]

                    game_records.append(game_record)
                else:
                    print("skipped game record")

    # remove duplicates
    temp_game_records = set(tuple(x) for x in game_records)
    game_records = [list(x) for x in temp_game_records]

    return game_records


def get_team_profile_stats(team):
    """
    Captures the team's stats from our csv file for them.
    :param team: team name
    :return: stats for the team
    """
    root_dir = '/Users/matt/Desktop/mnlacrossemodel/mnlacrossemodel/backend/data'
    profile_directory = root_dir + '/team_data/team-profiles/'
    filename = team + '~profile.csv'
    if filename in os.listdir(profile_directory):
        df = pd.read_csv(profile_directory + filename)
        stats = df.iloc[0]
        return stats
    else:
        print("Skipped game for: " + team)
        return None


def create_ml_dataset_csv(ml_dataset):
    """
    Creates the csv file that will contain all the records used in machine learning to predict game results.
    :param ml_dataset: the list of records
    """
    df = pd.DataFrame(ml_dataset, columns=[
            'home_team',
            'home_team_score',
            'home_team_record',
            'home_team_GFvGA',
            'away_team',
            'away_team_score',
            'away_team_record',
            'away_team_GFvGA',
            'winner',
            'year',
            'date'
        ])
    df.to_csv('/Users/matt/Desktop/mnlacrossemodel/mnlacrossemodel/backend/data/model_data/ml-dataset.csv')
    print(df)


if __name__ == "__main__":
    create_team_profiles()
    ml_dataset = create_records_for_ml_dataset()
    create_ml_dataset_csv(ml_dataset)
