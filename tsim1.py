import numpy as np
import random

def setup(m, avg_ctime):
    global occupy_turn, avgc, var
    avgc = avg_ctime
    occupy_turn = [0] * m
    var = 2


def get_comp_time(rank):
    delay_setting(rank)
    ctime = np.random.normal(avgc, var)
    ctime = max(ctime, avgc * 0.3)
    ctime = min(ctime, avgc * 2)
    if occupy_turn[rank] != 0:
        ctime *= 5
    return ctime


occupy_chance = 0.05
occupy_term_mean = 3
def delay_setting(rank):
    if occupy_turn[rank] == 0:
        if random.random() < occupy_chance:
            occupy_turn[rank] = int(np.random.normal(occupy_term_mean, 2))
    else:
        occupy_turn[rank] -= 1