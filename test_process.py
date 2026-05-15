import pytest
import pandas as pd
import numpy as np

from process import data_sample, get_gameweek, get_fixtures, get_result

@pytest.fixture
def test_data():

    df = pd.read_csv("data/test_data.csv")
    return df


def test_data_sample_gameweek_two_prev_games_five(test_data):
    
    """Test for trying to get a data sample from week 
    two using the previous 5 games' worth of data"""

    home = "West Ham"
    away = "Chelsea"

    with pytest.raises(Exception):
        data_sample(test_data, home, away)
        

def test_data_sample_gameweek_two_prev_games_three(test_data):

    """Test for trying to get a data sample from week
    two using the pevious 3 games' worth of data"""

    home = "Wolves"
    away = "Chelsea"

    with pytest.raises(Exception):
        data_sample(test_data, home, away, prev_games=3)


def test_data_sample_gameweek_five_prev_games_five(test_data):

    """Test for trying to get a data sample from week
    five using the previous 5 games' worth of data"""

    home = "Leicester"
    away = "Everton"

    with pytest.raises(Exception):
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

    result_one = get_result(test_data, "Wolves", "Chelsea")
    result_two = get_result(test_data, "Aston Villa", "Arsenal")
    result_three = get_result(test_data, "Brighton", "Ipswich")

    assert result_one == 1
    assert result_two == 0
    assert result_three == 0


def test_get_fixtures(test_data):

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