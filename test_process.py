import pytest
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from process import data_sample, get_gameweek, get_fixtures, get_result, create_datasets, get_BTTS_odds


@pytest.fixture
def test_data():

    df = pd.read_csv("data/processed.csv")
    return df


@pytest.fixture
def test_odds():

    df = pd.read_csv("data/betting_odds.csv")
    return df


def test_data_sample_gameweek_two_prev_games_five(test_data):
    
    """Test for trying to get a data sample from week 
    two using the previous 5 games' worth of data"""

    home = "West Ham"
    away = "Chelsea"

    with pytest.raises(Exception, match=r"Fixtures must be from gameweek"):
        data_sample(test_data, home, away)
        

def test_data_sample_gameweek_two_prev_games_three(test_data):

    """Test for trying to get a data sample from week
    two using the pevious 3 games' worth of data"""

    home = "Wolves"
    away = "Chelsea"

    with pytest.raises(Exception, match=r"Fixtures must be from gameweek"):
        data_sample(test_data, home, away, prev_games=3)


def test_data_sample_gameweek_five_prev_games_five(test_data):

    """Test for trying to get a data sample from week
    five using the previous 5 games' worth of data"""

    home = "Leicester"
    away = "Everton"

    with pytest.raises(Exception, match=r"Fixtures must be from gameweek"):
        data_sample(test_data, home, away)


def test_data_sample_two_prev_games(test_data):

    """Test for creating a data sample for Brentford vs West Ham using the 
    previous 2 games' worth of data"""

    data_df = data_sample(test_data, "Brentford", "West Ham", prev_games=2)

    brentford_total_goals = 1 + 1
    brentford_total_xg = 0.8 + 0.96
    brentford_total_xga = 3.52 + 2.17
    brentford_total_goals_conceded = 3 + 2
    brentford_home_factor = 0
    west_ham_total_goals = 0 + 1
    west_ham_total_xg = 0.85 + 0.76
    west_ham_total_xga = 2.19 + 1.54
    west_ham_total_goals_conceded = 3 + 1
    west_ham_away_factor = 0

    assert data_df["home_total_goals"].values == brentford_total_goals
    assert data_df["home_total_xg"].values == brentford_total_xg
    assert data_df["home_total_xga"].values == brentford_total_xga
    assert data_df["home_total_goals_conceded"].values == brentford_total_goals_conceded
    assert data_df["home_factor"].values == brentford_home_factor
    assert data_df["away_total_goals"].values == west_ham_total_goals
    assert data_df["away_total_xg"].values == west_ham_total_xg
    assert data_df["away_total_xga"].values == west_ham_total_xga
    assert data_df["away_total_goals_conceded"].values == west_ham_total_goals_conceded
    assert data_df["away_factor"].values == west_ham_away_factor


def test_data_sample_four_prev_games(test_data):

    """Test for creating a data sample for Arsenal vs Leicester using the previous
    4 games' worth of data"""

    data_df = data_sample(test_data, "Arsenal", "Leicester", prev_games=4)

    arsenal_total_goals = 2 + 1 + 1 + 2
    arsenal_total_xg = 0.87 + 2.14 + 0.67 + 0.74
    arsenal_total_xga = 0.71 + 2.18 + 1.28 + 1.76
    arsenal_total_goals_conceded = 1 + 2
    arsenal_home_factor = 0
    leicester_total_goals = 1 + 1 + 2 + 1
    leicester_total_xg = 0.61 + 0.45 + 1.23 + 0.66
    leicester_total_xga = 1.1 + 2.55 + 1.55 + 1.78
    leicester_total_goals_conceded = 2 + 2 + 2 + 1
    leicester_away_factor = (1 + 2) - (2 + 2)

    assert data_df["home_total_goals"].values == arsenal_total_goals
    assert data_df["home_total_xg"].values == arsenal_total_xg
    assert data_df["home_total_xga"].values == arsenal_total_xga
    assert data_df["home_total_goals_conceded"].values == arsenal_total_goals_conceded
    assert data_df["home_factor"].values == arsenal_home_factor
    assert data_df["away_total_goals"].values == leicester_total_goals
    assert data_df["away_total_xg"].values == leicester_total_xg
    assert data_df["away_total_xga"].values == leicester_total_xga
    assert data_df["away_total_goals_conceded"].values == leicester_total_goals_conceded
    assert data_df["away_factor"].values == leicester_away_factor


def test_get_gameweek(test_data):

    """Test for checking that the function returns the correct gameweek"""

    test_data_index = test_data.set_index("gameweek")

    gameweek_one = get_gameweek(test_data, "Ipswich", "Liverpool")
    gameweek_two = get_gameweek(test_data_index, "Wolves", "Chelsea")
    gameweek_three = get_gameweek(test_data, "Arsenal", "Brighton")
    gameweek_five = get_gameweek(test_data_index, "Tottenham", "Brentford")
    gameweek_six = get_gameweek(test_data, "Arsenal", "Leicester")

    assert gameweek_one ==1 
    assert gameweek_two == 2
    assert gameweek_three == 3
    assert gameweek_five == 5
    assert gameweek_six == 6
    

def test_get_result(test_data):

    "Test to check that the function returns the correct BTTS result for a game"

    result_one = get_result(test_data, "Wolves", "Chelsea")
    result_two = get_result(test_data, "Aston Villa", "Arsenal")
    result_three = get_result(test_data, "Brighton", "Ipswich")

    assert result_one == 1
    assert result_two == 0
    assert result_three == 0


def test_get_fixtures(test_data):

    """Test to check that the function returns the correct fixtures for a given gameweek"""

    home_teams = ["Manchester United", "Ipswich", "Arsenal", "Everton", "Newcastle United", "Nottingham Forest",
                  "West Ham", "Brentford", "Chelsea", "Leicester"]
    away_teams = ["Fulham", "Liverpool", "Wolves", "Brighton", "Southampton", "Bournemouth", "Aston Villa",
                  "Crystal Palace", "Manchester City", "Tottenham"]
    
    fixtures = get_fixtures(test_data, 1)
    fixtures_home_teams = []
    fixtures_away_teams = []

    for i, j in fixtures:

        fixtures_home_teams.append(i)
        fixtures_away_teams.append(j)

    assert fixtures_home_teams == home_teams
    assert fixtures_away_teams == away_teams


def test_create_datasets_start_week_less_than_two(test_data):

    """Tests the function when the start week in less than two"""
    
    with pytest.raises(Exception, match=r"Start week must be in {2, 3, 4, ..., 37}"):
        create_datasets(test_data, start_week=1, test_week=30)


def test_create_datasets_start_week_greater_than_thirty_seven(test_data):

    """Tests the function when the start week is greater than 37"""

    with pytest.raises(Exception, match=r"Start week must be in {2, 3, 4, ..., 37}"):
        create_datasets(test_data, start_week=38, test_week=38)


def test_create_datasets_test_week_less_than_start_week_plus_one(test_data):

    """Tests the function when the test week is not greater than the start week"""

    with pytest.raises(Exception, match=r"Test week must be after start week and not greater than 38"):
        create_datasets(test_data, start_week=2, test_week=2)


def test_create_datasets_test_week_greater_than_thirty_eight(test_data):

    """Tests the function when the test week is greater than 38"""

    with pytest.raises(Exception, match=r"Test week must be after start week and not greater than 38"):
        create_datasets(test_data, start_week=36, test_week=39)


def test_create_datasets(test_data):

    """Tests the function returns the correct output for valid inputs"""

    training_samples = []
    sc = StandardScaler()
    for i in range(6, 15):
        training_fixtures = get_fixtures(test_data, i)

        for home, away in training_fixtures:
            training_samples.append(data_sample(test_data, home, away))

    training_samples_df = pd.concat(training_samples)
    X_train_df = training_samples_df.drop("BTTS result", axis=1)
    X_train = sc.fit_transform(X_train_df)
    y_train = training_samples_df["BTTS result"].values

    testing_fixtures = get_fixtures(test_data, 15)
    testing_samples = [data_sample(test_data, home, away) for home, away in testing_fixtures]
    testing_samples_df = pd.concat(testing_samples)
    X_test_df = testing_samples_df.drop("BTTS result", axis=1)
    X_test = sc.fit_transform(X_test_df)
    y_test = testing_samples_df["BTTS result"].values

    res1, res2, res3, res4 = create_datasets(test_data, start_week=6, test_week=15)

    np.testing.assert_array_equal(X_train, res1)
    np.testing.assert_array_equal(y_train, res2)
    np.testing.assert_array_equal(X_test, res3)
    np.testing.assert_array_equal(y_test, res4)


def test_get_BTTS_odds_gameweek_less_than_one(test_data, test_odds):

    """Tests the function when gameweek is less than one"""

    with pytest.raises(Exception, match=r"gameweek must be in {1, 2, 3, ..., 38}"):
        get_BTTS_odds(test_data, test_odds, 0)


def test_get_BTTS_odds_gameweek_less_than_one(test_data, test_odds):

    """Tests the function when gameweek is greater than 38"""

    with pytest.raises(Exception, match=r"gameweek must be in {1, 2, 3, ..., 38}"):
        get_BTTS_odds(test_data, test_odds, 39)


def test_get_BTTS_odds_gameweek_thirty_eight(test_data, test_odds):

    """Tests the function returns correct output for valid inputs"""

    home_teams = ["Bournemouth", "Fulham", "Ipswich", "Liverpool", "Manchester United", "Newcastle United",
                  "Nottingham Forest", "Southampton", "Tottenham", "Wolves"]
    away_teams = ["Leicester", "Manchester City", "West Ham", "Crystal Palace", "Aston Villa", "Everton",
                  "Chelsea", "Arsenal", "Brighton", "Brentford"]
    btts_yes = [1.72, 1.65, 1.62, 1.52, 1.6, 1.76, 1.6, 1.83, 1.48, 1.48]
    btts_no = [2.12, 2.24, 2.31, 2.54, 2.34, 2.06, 2.34, 1.98, 2.68, 2.68]

    expected_odds = list(zip(home_teams, away_teams, btts_yes, btts_no))

    assert list(get_BTTS_odds(test_data, test_odds, 38)) == expected_odds