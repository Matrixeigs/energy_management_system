# Defalut parameters of generation model
import configuration.configuration_time_line as timeline

default_AC_generator_parameters = \
    {
        "AREA": 1,
        "GEN_STATUS": 1,  # The generation status, >0 means avalible, otherwise, unavaliable
        "PG": 0,
        "QG": 0,
        "PMAX": 3000,
        "PMIN": 0,
        "QMAX": 3000,
        "QMIN": -3000,
        "SMAX": 3000,
        "VG": 1.0,
        "RAMP_AGC": 3000,
        "RAMP_10": 3000,
        "PF_LIMIT": [-1, 1],
        "APF": 0,  # The droop parameters
        "COST_START_UP": 0,
        "COST_SHUT_DOWN": 0,
        "COST_MODEL": 2,
        "NCOST": 3,
        "COST": [0.01, 2.0, 4.0],
        "TIME_GENERATED": timeline.default_time["Base_time"],
        "TIME_APPLIED": [timeline.default_time["Base_time"], timeline.default_time["Look_ahead_time_uc"]],
        "TIME_COMMANDED": timeline.default_time["Base_time"],
        "COMMAND_START_UP": 0,
        "COMMAND_SET_POINT_VG": 0,
        "COMMAND_SET_POINT_PG": 0,
        "COMMAND_SET_POINT_QG": 0,
        "COMMAND_RESERVE": 0
    }


default_DC_generator_parameters = \
    {
        "AREA": 1,
        "GEN_STATUS": 1,  # The generation status, >0 means avalible, otherwise, unavaliable
        "PG": 0,
        "PMAX": 3000,
        "PMIN": 0,
        "VG": 1.0,
        "RAMP_AGC": 3000,
        "RAMP_10": 3000,
        "APF": 0,  # The droop parameters
        "COST_START_UP": 0,
        "COST_SHUT_DOWN": 0,
        "COST_MODEL": 2,
        "NCOST": 3,
        "COST": [0.01, 2.0, 4.0],
        "TIME_GENERATED": timeline.default_time["Base_time"],
        "TIME_APPLIED": [timeline.default_time["Base_time"], timeline.default_time["Look_ahead_time_uc"]],
        "TIME_COMMANDED": timeline.default_time["Base_time"],
        "COMMAND_START_UP": 0,
        "COMMAND_SET_POINT_VG": 0,
        "COMMAND_SET_POINT_PG": 0,
        "COMMAND_RESERVE": 0
    }

default_RES_generator_parameters = \
    {
        "AREA": 1,
        "TYPE": 1,
        "GEN_STATUS": 1,  # The generation status, >0 means avalible, otherwise, unavaliable
        "PG": 0,
        "QG": 0,
        "PMAX": 0000,
        "PMIN": 0,
        "QMAX": 3000,
        "QMIN": -3000,
        "SMAX": 3000,
        "COST": 1000,
        "TIME_GENERATED": timeline.default_time["Base_time"],
        "TIME_APPLIED": [timeline.default_time["Base_time"], timeline.default_time["Look_ahead_time_uc"]],
        "TIME_COMMANDED": timeline.default_time["Base_time"],
        "COMMAND_CURT": 0,
        "COMMAND_SET_POINT_PG": 0,
    }