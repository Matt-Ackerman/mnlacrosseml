TO RUN APP:

    python3 manage.py runserver

TODO:

A chron job runs once every day:
    1. grabs the gameday from the slider that just happened
    2. adds to past predictions table with the prediction and correctness of it
    1. grabs the next existing gameday from gameday slider
    2. populates the upcoming table with it
    
    
all the website does is show the gameday that shows up automatically on the hubs slider page
    1. puts all the games for that day into the upcoming games table along with a prediction
    2. appends all the games for the last gameday into the p
    
    the chron job, which runs each day at 10 am, creates it 



    1. capture actual past game results and add them to past-predictions.csv
    2. add them to the ml-dataset.csv as well
    
    when the app is ran
        1. every day at 5 pm, it updates to grab predictions for the next 2 days and stores them in an 'upcoming-predictions' file
        2. it grabs the games from upcoming-predictions, finds their results in laxhub, and moves them to a 'past-predictions' file
        3. every time a user enters the app, i show them the upcoming-predictions file and the past-predictions file
        4. also, needs to somehow update our model_data so it experiences newly played games
    
    
 
    LIVE WEBSITE
    -------------
    3. a. Every time a user enters the website, the entry function will grab all games from
          list 1 whose date is within today and tomorrow.
       b. It will create a predicted outcome and spread for the game, 
          and add it to the front end table titled "upcoming games".
       c. The entry function will also check each teams page on mnlaxhub to grab games that have now
          occured. It will show another front end table titled "past games" that shows the prediction correctness.
    
       
    UI Ideas
    --------
    3 tabs. Opens the website on second tab.
        Tab 1. All past predictions in one long list.
        Tab 2. All predictions for next couple days.
        Tab 3. Methodology / contact info


mn-lacrosse-ml
--------------
The goal is to combine into one record each past game result with the profile stats of the competing teams.
Then, in the future, when we want to predict the result of an upcoming game, our ml algorithm will be able to identify
the likelihood of a winner given the historical outcomes of two teams competing with similar profile stats.

    data_ingest.py
    --------------
    Scrapes data from the web to capture game results. Loops through a list of conference homepages (twice. once for 2018 and once for 2019)
    and creates a dictionary of {team : team main page url}. We then loop through the dictionary and go to each team
    main page url. From there, we capture the url to that team's schedule results and replace the value in the
    aforementioned dictionary. We loop through the dictionary again, going to the schedule results page for each team and
    creating a dictionary of a list of lists {team : [[result1 stats], [result2 stats], ..}. Since we've completed all
    the previous steps twice (2018 and 2019), we now merge the list of lists dictionary for both into one dictionary. We
    finally create a csv file for each team's combined 2018 and 2019 schedule.

    data_prep.py
    ------------
    Utilizes the now ingested data to prepare for machine learning. We start by creating a profile csv for each team.
    Each profile contains the stats necessary for our ml algorithm to work effectively. We then loop through each game from
    each team schedule, (created by data-ingest.py) check the profile stats of the competing teams, and combine them into
    one record. These records are added to a list of lists. Once we remove the duplicates caused by our capture process,
    we create a csv from the list that now contains every game played in the state. This csv file is what we will train
    our ml algorithm on.

General info:
-------------
- What modeling strategies did we look into and what did we use and why?
- How do we account for lack of data on a team to start the season? Answer: Creating team profiles with the last two years
  data for the school. Then (hopefully) weighing recent games more. Or, adding current season performance as its own metric.