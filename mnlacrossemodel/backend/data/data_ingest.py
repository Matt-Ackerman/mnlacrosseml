import requests
import json as js
import pandas as pd
from bs4 import BeautifulSoup


def gather_all_team_schedules_from_conference(conference):
    """
    Loops through the team_data in a conference and returns a dict with their team name and the url for their main page.
    :param conference: the url for the conference page where we get the team_data from.
    :return: {team name : team main page url}
    """
    # what we will return. a dict of team name to team url
    teams = {}

    page = requests.get(conference)
    html = page.text

    # table is in javascript so we can't use Soup
    for line in html.splitlines():
        if "var pageNav = {" in line:
            index = line.index("var pageNav = {")
            json_string = line[index+14: len(line)-1]
            json = js.loads(json_string)
            teams_json = json["children"]
            for team in teams_json:
                teams[team["name"]] = "https://www.mnlaxhub.com" + team["url"]

    # go to each team_data main page and get link to schedule page. replace val with schedule link.
    for key, value in teams.items():
        page = requests.get(value)
        soup = BeautifulSoup(page.content, 'html.parser')
        schedule = soup.find(id='tool-game-schedule')
        if schedule is None:
            teams[key] = None
            print(key + " has no schedule")
        else:
            schedule_url = schedule.find('a', class_='remote-tool-tab')
            season_sched = schedule_url.attrs["href"]
            teams[key] = "https://www.mnlaxhub.com" + season_sched

    return teams


def retrieve_schedule_results(teams, year):
    """
    From the team's schedule url, go through their schedule and add it to the team-schedule-results dict.
    :param teams: {team name : team schedule url}
    :return: {
        team name : [[game result 1], [game result 2], [game result 3], ...],
        team name : ...
    }
    """
    # team name to schedule team-schedule-results
    team_to_schedule_results_dict = {}

    # will be an array of arrays. each array is a game result.
    schedule_results = []

    for key, value in teams.items():
        if value is not None:
            page = requests.get(value)
            soup = BeautifulSoup(page.content, 'html.parser')
            game_list = soup.find(id='tab_completegamelist_content')

            table = game_list.find('table', class_='statTable sortable noSortImages')
            games = table.find_all('tr', class_='odd completed compactGameList')
            games = games + table.find_all('tr', class_='even completed compactGameList')
            # loop through each game result in the table
            for game in games:
                opp_name = game.find('div', class_='scheduleListTeam').text
                result = game.find('div', class_='scheduleListResult').text
                score = game.find('a', class_='game_link_referrer').text
                date = game.find('td', class_='nowrap').text
                # data cleanse
                if '@' in opp_name:
                    location = 'Away'
                    opp_name = opp_name.replace("@", "")
                else:
                    location = 'Home'

                opp_name = opp_name.replace("'", "").replace("/", " ").replace("\n", "").lstrip().rstrip()
                result = result.replace(" ", "").replace("\n", "")
                score = score.replace(" ", "").replace("\n", "")
                date = date.replace("\n", "").lstrip().rstrip()
                goals_for = score[0:score.index('-')]
                goals_against = score[score.index('-')+1:len(score)]

                schedule_results.append([opp_name, goals_for, goals_against, result, location, year, date])

            # if a team had less than 5 games, we will leave the schedule out
            if len(schedule_results) > 5:
                team_to_schedule_results_dict[key] = schedule_results

            # reset for next team
            schedule_results = []

    return team_to_schedule_results_dict


def retrieve_schedules_2020(teams):
    """
    From the team's upcoming 2020 schedule url, go through their schedule and add each game to the team-schedule dict.
    :param teams: {team name : team schedule url}
    """
    # team name to schedule team-schedule-results
    team_to_schedule_dict = {}

    # will be an array of arrays. each array is a game result.
    schedule_results = []

    for key, value in teams.items():
        if value is not None:
            page = requests.get(value)
            soup = BeautifulSoup(page.content, 'html.parser')
            game_list = soup.find(id='tab_completegamelist_content')

            table = game_list.find('table', class_='statTable sortable noSortImages')
            games = table.find_all('tr', class_='odd scheduled compactGameList')
            games = games + table.find_all('tr', class_='even scheduled compactGameList')
            # loop through each game result in the table
            for game in games:
                opp_name = game.find('div', class_='scheduleListTeam').text
                date = game.find('td', class_='nowrap').text
                # data cleanse
                if '@' in opp_name:
                    location = 'Away'
                    opp_name = opp_name.replace("@", "")
                else:
                    location = 'Home'

                opp_name = opp_name.replace("'", "").replace("/", " ").replace("\n", "").lstrip().rstrip()
                date = date.replace("\n", "").lstrip().rstrip()

                schedule_results.append([opp_name, location, date])

            # if a team had less than 5 games, we will leave the schedule out
            if len(schedule_results) > 5:
                team_to_schedule_dict[key] = schedule_results

            # reset for next team
            schedule_results = []

    return team_to_schedule_dict


def merge_years(year1, year2):
    """
    Merges dictionaries and keeps values of common keys ijnj list.
    :param year1: first dict.
    :param year2: second dict.
    :return: the merged dicts.
    """
    ''' Merge dictionaries and keep values of common keys in list'''
    for key, value in year2.items():
        if key in year1:
            for game in value:
                year1[key].append(game)
        else:
            year1[key] = value

    return year1


def create_2020_total_state_schedule(team_schedules2020):
    all_2020_games = []
    for team in team_schedules2020:
        for game in team_schedules2020.get(team):
            team = team.replace("'", "").lstrip().rstrip()
            opp_team = game[0].replace("'", "").lstrip().rstrip()
            if game[1] is 'Home':
                all_2020_games.append([team, opp_team, game[2]])
            else:
                all_2020_games.append([opp_team, team, game[2]])

    # remove duplicates
    temp_games = set(tuple(x) for x in all_2020_games)
    games = [list(x) for x in temp_games]

    return games


def create_schedule_results_csv(sched_results):
    """
    Creates a csv file for each team with their schedule team-schedule-results.
    :param sched_results: schedule team-schedule-results.
    """
    for team in sched_results:
        df = pd.DataFrame(sched_results[team], columns=['Opponent', 'Goals For', 'Goals Against', 'Result', 'Location', 'Year', 'Date'])
        df.to_csv('team_data/team-schedule-results/' + team.replace('/', ' ').replace("'", '').rstrip() + '~team-schedule-results.csv')
        print(df)


def create_2020_schedules_csv(sched_results):
    """
    Creates a csv file for each team with their schedule team-schedule-results.
    :param sched_results: schedule team-schedule-results.
    """
    for team in sched_results:
        df = pd.DataFrame(sched_results[team], columns=['Opponent', 'Location', 'Date'])
        df.to_csv('team_data/team-2020-schedules/' + team.replace('/', ' ').replace("'", '').rstrip() + '~team-2020-schedule.csv')
        print(df)


def create_2020_total_state_schedule_csv(schedule_2020):
    """
    Creates the csv file that will contain all the 2020 games.
    :param schedule_2020
    """
    df = pd.DataFrame(schedule_2020, columns=[
            'home_team',
            'away_team',
            'date'
        ])
    df.to_csv('team_data/2020-complete-schedule/2020-schedule.csv')
    print(df)


# if __name__ == "__main__":
#     conferences_2020 = [
#         "https://www.mnlaxhub.com/page/show/5590474-big-9",
#         "https://www.mnlaxhub.com/page/show/5590481-greater-west-metro",
#         "https://www.mnlaxhub.com/page/show/5590492-imac",
#         "https://www.mnlaxhub.com/page/show/5590498-independent",
#         "https://www.mnlaxhub.com/page/show/5590510-lake",
#         "https://www.mnlaxhub.com/page/show/5590517-metro-east",
#         "https://www.mnlaxhub.com/page/show/5590526-metro-west",
#         "https://www.mnlaxhub.com/page/show/5590534-northwest-suburban",
#         "https://www.mnlaxhub.com/page/show/5590549-south-suburban",
#         "https://www.mnlaxhub.com/page/show/5590563-suburban-east",
#         "https://www.mnlaxhub.com/page/show/5590576-wright-county"
#     ]
#
#     teams2020 = {}
#
#     # loop through conferences and add all the team_data to our dict
#     for conference in conferences_2020:
#         teams2020 = {**teams2020, **gather_all_team_schedules_from_conference(conference)}
#
#     team_schedules2020 = retrieve_schedules_2020(teams2020)
#
#     # create_2020_schedules_csv(team_schedules2020)
#
#     complete_2020_schedule = create_2020_total_state_schedule(team_schedules2020)
#     create_2020_total_state_schedule_csv(complete_2020_schedule)


# if __name__ == "__main__":
#     conferences_2019 = [
#         "https://www.mnlaxhub.com/page/show/4829476-big-9",
#         "https://www.mnlaxhub.com/page/show/4829483-greater-west-metro",
#         "https://www.mnlaxhub.com/page/show/4829497-imac",
#         "https://www.mnlaxhub.com/page/show/4829503-independent",
#         "https://www.mnlaxhub.com/page/show/4829515-lake",
#         "https://www.mnlaxhub.com/page/show/4829523-metro-east",
#         "https://www.mnlaxhub.com/page/show/4829531-metro-west",
#         "https://www.mnlaxhub.com/page/show/4829539-northwest-suburban",
#         "https://www.mnlaxhub.com/page/show/4829554-south-suburban",
#         "https://www.mnlaxhub.com/page/show/4829568-suburban-east",
#         "https://www.mnlaxhub.com/page/show/4957820-wright-county"
#     ]
#
#     conferences_2018 = [
#         "https://www.mnlaxhub.com/page/show/3537590-big-9",
#         "https://www.mnlaxhub.com/page/show/3537597-greater-west-metro",
#         "https://www.mnlaxhub.com/page/show/3537608-imac",
#         "https://www.mnlaxhub.com/page/show/3537614-independent",
#         "https://www.mnlaxhub.com/page/show/3537624-lake",
#         "https://www.mnlaxhub.com/page/show/3537631-metro-east",
#         "https://www.mnlaxhub.com/page/show/3537639-metro-west",
#         "https://www.mnlaxhub.com/page/show/3537647-northwest-suburban",
#         "https://www.mnlaxhub.com/page/show/3537662-south-suburban",
#         "https://www.mnlaxhub.com/page/show/3537676-suburban-east"
#     ]
#
#     teams2018 = {}
#     teams2019 = {}
#
#     # loop through conferences and add all the team_data to our dict
#     for conference in conferences_2018:
#         teams2018 = {**teams2018, **gather_all_team_schedules_from_conference(conference)}
#
#     for conference in conferences_2019:
#         teams2019 = {**teams2019, **gather_all_team_schedules_from_conference(conference)}
#
#     # getting team-schedule-results of the schedule from the url
#     results2018 = retrieve_schedule_results(teams2018, '2018')
#     results2019 = retrieve_schedule_results(teams2019, '2019')
#
#     results2018and2019 = merge_years(results2018, results2019)
#     # create_schedule_results_csv(results2018and2019)

