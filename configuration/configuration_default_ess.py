"""
Default parameters of the energy storage systems.
The dictionary is used.
"""
import configuration.configuration_time_line as timeline

BESS = \
    {
        "AREA": 1,
        "CAP": 10000,
        "PMAX_DIS": 1000,
        "PMAX_CH": 1000,
        "EFF_DIS": 0.95,
        "EFF_CH": 0.95,
        "SOC_MAX": 1,
        "SOC_MIN": 0.1,
        "SOC": 0.5,
        "COST_MODEL": 1,
        "NCOST_DIS": 1,
        "COST_DIS": [1],
        "NCOST_CH": 1,
        "COST_CH": [1],
        "TIME_GENERATED": timeline.default_time["Base_time"],
        "TIME_APPLIED": [timeline.default_time["Base_time"], timeline.default_time["Look_ahead_time_uc"]],
        "TIME_COMMANDED": timeline.default_time["Base_time"],
        "COMMAND_PG": 0,
        "COMMAND_RG": 0,
    }
