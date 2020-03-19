TO RUN APP:

    python3 manage.py runserver

TODO:
    
    DATA PREP
    ---------
    1. a. Create 1 massive list of played games for this season. This will start empty.
       b. Each game in massive list will include date, team names, prediction outcome, spread prediction, whatever.
    
    LIVE WEBSITE
    -------------
    3. a. Every time a user enters the website, the entry function will grab all games from
          list 1 whose date is within today and tomorrow.
       b. It will create a predicted outcome and spread for the game, 
          and add it to the front end table titled "upcoming games".
       c. The entry function will also check each teams page on mnlaxhub to grab games that have now
          occured. It will show another front end table titled "past games" that shows the prediction correctness.
    
       
    
    We will check what games are happening over the next
    two days, and add them along with their prediction 
    to a table.
    
    We will also have another table that contains all the
    games that have occured this season along with our prediction
    correctness results.
    
    
    -----
    1. Decide how to check results of games, load them into
       our predictor records, and update the website with
       the results of our predictions
    2. Create UI table that shows games for the next
       two or three days as well as their predictions
       
       
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