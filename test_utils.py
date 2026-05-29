from utils import convert_btts_odds_to_probability
import pytest


def test_convert_btts_odds_to_probability_less_than_one():

    """Test the function when BTTS odds are less than one"""

    with pytest.raises(Exception, match=r"BTTS cannot be less than one"):
        convert_btts_odds_to_probability(0.99)


def test_convert_btts_odds_to_probability_valid_float():
    
    """Tests the function when BTTS odds are a valid float"""

    assert 1/2.12 == convert_btts_odds_to_probability(2.12)