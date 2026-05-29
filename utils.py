def convert_btts_odds_to_probability(btts: float) -> float:

    """Calculates the implied probability from BTTS"""

    if btts < 1:
        raise Exception("BTTS cannot be less than one")

    return 1/btts    