import pandas as pd
from sklearn.preprocessing import StandardScaler


def create_datasets(data_df: pd.DataFrame, start_week: int, test_week: int,  prev_games: int = 5, scale: bool = True) -> tuple:

    """Function for creating the training and testing datasets. Designed for testing one week's set of fixtures at a time."""

    if (start_week < 2 or start_week > 37):
        raise Exception("Start week must be in {2, 3, 4, ..., 37}")
    
    if (test_week < start_week + 1 or test_week > 38):
        raise Exception("Test week must be after start week and not greater than 38")
    
    training_samples = []
    # get the data samples for each week in the given range 
    training_fixtures = [get_fixtures(data_df, gameweek) for gameweek in range(start_week, test_week)]
    for round in training_fixtures:
        round_samples = [data_sample(data_df, home, away, prev_games) for home, away in round]
        training_samples += round_samples

    training_samples_df = pd.concat(training_samples)

    # extract X and y from the training data
    y_train = training_samples_df["BTTS result"].values
    X_train_df = training_samples_df.drop("BTTS result", axis=1)    

    if scale == True:
        sc = StandardScaler()
        X_train = sc.fit_transform(X_train_df)
    
    else:
        X_train = X_train_df.to_numpy()

    # get the test data
    testing_fixtures = get_fixtures(data_df, test_week)
    testing_samples = [data_sample(data_df, home, away) for home, away in testing_fixtures]
    testing_samples_df = pd.concat(testing_samples)
    X_test_df = testing_samples_df.drop("BTTS result", axis=1)

    if scale == True:
        X_test = sc.fit_transform(X_test_df)

    else:
        X_test = X_test_df.to_numpy()

    y_test = testing_samples_df["BTTS result"].values

    return X_train, y_train, X_test, y_test


def data_sample(data_df: pd.DataFrame, home_team: str, away_team: str, prev_games: int = 5) -> pd.DataFrame:

    """Produces a data sample for given home and away teams"""
    
    data_df = data_df.set_index("gameweek")
    gameweek = get_gameweek(data_df, home_team, away_team)
    if gameweek <= prev_games:
        raise Exception("Fixtures must be from gameweek {} or later in order for data to be accumulated".format(prev_games+1))
    
    result = get_result(data_df, home_team, away_team)
    # reduce the dataframe to the prevous 5 games
    data_df_red = data_df.loc[gameweek-prev_games:gameweek-1]
    # get the past home and away games for the home and away teams
    home_team_home = data_df_red.loc[(data_df_red["home_team"] == home_team)]
    home_team_away = data_df_red.loc[(data_df_red["away_team"] == home_team)]
    away_team_home = data_df_red.loc[(data_df_red["home_team"] == away_team)]
    away_team_away = data_df_red.loc[(data_df_red["away_team"] == away_team)]
    # compile the totals dataframe
    totals_dict = {}
    totals_dict["home_total_goals"] = sum(home_team_home["home_score"]) + sum(home_team_away["away_score"])
    totals_dict["home_total_xg"] = sum(home_team_home["home_expected_goals_xg"]) + sum(home_team_away["away_expected_goals_xg"])
    totals_dict["home_total_xga"] = sum(home_team_home["away_expected_goals_xg"]) + sum(home_team_away["home_expected_goals_xg"])
    totals_dict["home_total_goals_conceded"] = sum(home_team_home["away_score"]) + sum(home_team_away["home_score"])
    totals_dict["home_factor"] = sum(home_team_home["home_score"])-sum(home_team_home["away_score"])
    totals_dict["away_total_goals"] = sum(away_team_home["home_score"]) + sum(away_team_away["away_score"])
    totals_dict["away_total_xg"] = sum(away_team_home["home_expected_goals_xg"]) + sum(away_team_away["away_expected_goals_xg"])
    totals_dict["away_total_xga"] = sum(away_team_home["away_expected_goals_xg"]) + sum(away_team_away["home_expected_goals_xg"])
    totals_dict["away_total_goals_conceded"] = sum(away_team_home["away_score"]) + sum(away_team_away["home_score"])
    totals_dict["away_factor"] = sum(away_team_away["away_score"]) - sum(away_team_away["home_score"])
    totals_dict["BTTS result"] = result
    totals_df = pd.DataFrame(totals_dict, index=[0])

    return totals_df


def get_gameweek(data_df: pd.DataFrame, home_team: str, away_team: str) -> int:

    """Identifies the gameweek corresponding to a given fixture"""

    data_df = data_df.loc[(data_df["home_team"] == home_team)]
    data_df = data_df.loc[(data_df["away_team"] == away_team)]

    if "gameweek" in data_df.columns:
        return data_df["gameweek"].values
    
    else:
        return data_df.index[0]


def get_result(data_df: pd.DataFrame, home_team: str, away_team: str) -> int:

    """Identifies whether or not both teams have scored in a game or not"""

    data_df = data_df.loc[(data_df["home_team"] == home_team)]
    data_df = data_df.loc[(data_df["away_team"] == away_team)]

    home_score = data_df["home_score"].values[0]
    away_score = data_df["away_score"].values[0]

    if (home_score > 0 and away_score > 0):        
         return 1
    
    else:
        return 0


def get_fixtures(data_df: pd.DataFrame, gameweek: int) -> zip:

    """Returns all fixtures for a given gameweek"""

    data_df = data_df.set_index("gameweek")
    data_df = data_df.loc[gameweek]
    home_teams = []
    away_teams = []
    for index, row in data_df.iterrows():
        home_teams.append(row["home_team"])
        away_teams.append(row["away_team"])

    return zip(home_teams, away_teams)


def get_BTTS_odds(data_df: pd.DataFrame, odds_df: pd.DataFrame, gameweek: int) -> zip:

    """Returns fixtures and BTTS odds for a given gameweek"""

    if (gameweek < 1 or gameweek > 38):
        raise Exception("gameweek must be in {1, 2, 3, ..., 38}")

    home_teams = []
    away_teams = []
    btts_yes = []
    btts_no = []

    fixtures = get_fixtures(data_df, gameweek)
    for home, away in fixtures:
        all_home = odds_df[odds_df["homeTeam"] == home]
        match = all_home[all_home["awayTeam"] == away]
        btts_yes.append(match["BTTSY"].values.item())
        btts_no.append(match["BTTSN"].values.item())
        home_teams.append(home)
        away_teams.append(away)

    return zip(home_teams, away_teams, btts_yes, btts_no)

