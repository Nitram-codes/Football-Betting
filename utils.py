import pandas as pd
import numpy as np


def convert_btts_odds_to_probability(btts: float) -> float:

    """Calculates the implied probability from BTTS"""

    if btts < 1:
        raise Exception("BTTS cannot be less than one")

    return 1/btts    


def get_results(data_df: pd.DataFrame, gameweek: int) -> pd.DataFrame:

    """Returns the fixtures and results of a given gameweek"""

    filtered = data_df[data_df["gameweek"] == gameweek]
    filtered = filtered[["home_team", "home_score", "away_score", "away_team"]]
    filtered["btts"] = np.where((filtered["home_score"] > 0) & (filtered["away_score"] > 0), True, False)
    
    return filtered