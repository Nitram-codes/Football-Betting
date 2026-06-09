from utils import convert_btts_odds_to_probability, get_results
from pandas.testing import assert_frame_equal
import pandas as pd
import pytest


@pytest.fixture
def test_data():

    df = pd.read_csv("data/processed.csv")
    return df


def test_convert_btts_odds_to_probability_less_than_one():

    """Test the function when BTTS odds are less than one"""

    with pytest.raises(ValueError, match=r"BTTS cannot be less than one"):
        convert_btts_odds_to_probability(0.99)


def test_convert_btts_odds_to_probability_valid_float():
    
    """Tests the function when BTTS odds are a valid float"""

    assert 1/2.12 == convert_btts_odds_to_probability(2.12)


def test_get_results_gameweek_less_than_one(test_data):

    """Tests the function when gameweek is less than one"""

    with pytest.raises(ValueError, match=r"gameweek must be in {1, 2, 3, ..., 38}"):
        get_results(test_data, 0)


def test_get_results_gameweek_greater_than_thirty_eight(test_data):

    """Tests the function when gameweek is greater than 38"""

    with pytest.raises(ValueError, match=r"gameweek must be in {1, 2, 3, ..., 38}"):
        get_results(test_data, 39)


def test_get_results_gameweek_twenty_five(test_data):

    """Tests the function for gameweek 25"""

    home_teams = ["Brighton", "Leicester", "Aston Villa", "Fulham", "Manchester City", "Southampton",
                  "West Ham", "Crystal Palace", "Liverpool", "Tottenham", "Aston Villa"]
    away_teams = ["Chelsea", "Arsenal", "Ipswich", "Nottingham Forest", "Newcastle United", "Bournemouth",
                  "Brentford", "Everton", "Wolves", "Manchester United", "Liverpool"]
    home_goals = [3, 0, 1, 2, 4, 1, 0, 1, 2, 1, 2]
    away_goals = [0, 2, 1, 1, 0, 3, 1, 2, 1, 0, 2]
    btts = [False, False, True, True, False, True, False, True, True, False, True]

    expected_df = pd.DataFrame({"home team": home_teams, "home score": home_goals, "away score": away_goals, 
                                "away team": away_teams, "btts": btts})
    actual_df = get_results(test_data, 25)

    assert_frame_equal(expected_df, actual_df)