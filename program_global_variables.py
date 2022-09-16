from enum import Enum

co2_values_rebaseline = []
co2_upper_bound = 1300
co2_lower_bound = 1050

class ProgMode(Enum):
    AVG_CASE = 1
    WORST_CASE = 2

prog_mode = ProgMode.WORST_CASE

