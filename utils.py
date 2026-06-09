import pandas as pd
import numpy as np


def convert_btts_odds_to_probability(btts: float) -> float:

    """Calculates the implied probability from BTTS"""

    if btts < 1:
        raise ValueError("BTTS cannot be less than one")

    return 1/btts    


def get_results(data_df: pd.DataFrame, gameweek: int) -> pd.DataFrame:

    """Returns the fixtures and results of a given gameweek"""

    if (gameweek < 1 or gameweek > 38):
        raise ValueError("gameweek must be in {1, 2, 3, ..., 38}")

    filtered = data_df[data_df["gameweek"] == gameweek]
    filtered = filtered[["home_team", "home_score", "away_score", "away_team"]]
    filtered["btts"] = np.where((filtered["home_score"] > 0) & (filtered["away_score"] > 0), True, False)
    filtered = filtered.rename(columns = {"home_team": "home team", "home_score": "home score", "away_score": "away score",
                               "away_team": "away team"})
    filtered = filtered.reset_index(drop=True)
    
    return filtered