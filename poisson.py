import math
import numpy as np

def poisson_calc(goals, expected_goals):

    prob = expected_goals**goals * np.exp(-expected_goals) / math.factorial(goals)

    return prob