import math
import numpy as np

def poisson_calc(goals: int, expected_goals: float) -> float: 

    """Computes the Poisson pmf"""

    prob = expected_goals**goals * np.exp(-expected_goals) / math.factorial(goals)

    return prob