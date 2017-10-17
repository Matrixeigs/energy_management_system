# default parameters of loads
import configuration.configuration_time_line as timeline

default_Load_AC = \
    {
        "AREA": 1,
        "STATUS": 1,  # The generation status, >0 means avalible, otherwise, unavaliable
        "PD": 0,
        "QD": 0,
        "PF":1,
        "PDMAX": 1000,
        "PDMIN": 0,
        "FLEX": 0,# 0, load is undispatchable;1, load is dispatchable
        "APF":0,
        "MODEL": 1,# 0, load is discrete dispatchable;1, load is contineously dispatchable
        "COST_MODEL": 2,
        "NCOST": 3,
        "COST": [1000, 2.0, 4.0],
        "PROFILE": [1000, 2000, 3000, 2000, 2000, 3000, 1000, 500, 400],
        "TIME_GENERATED": timeline.default_time["Base_time"],
        "TIME_APPLIED": [timeline.default_time["Base_time"], timeline.default_time["Look_ahead_time_uc"]],
        "TIME_COMMANDED": timeline.default_time["Base_time"],
        "COMMAND_SHED": 0,
        "COMMAND_RESERVE":0,
    }

default_Load_DC = \
    {
        "AREA": 1,
        "STATUS": 1,  # The generation status, >0 means avalible, otherwise, unavaliable
        "PD": 0,
        "PF":1,
        "PDMAX": 1000,
        "PDMIN": 0,
        "FLEX": 0,# 0, load is undispatchable;1, load is dispatchable
        "APF":0,
        "MODEL": 1,# 0, load is discrete dispatchable;1, load is contineously dispatchable
        "COST_MODEL": 2,
        "NCOST": 3,
        "COST": [1000, 2.0, 4.0],
        "PROFILE": [1000, 2000, 3000, 2000, 2000, 3000, 1000, 500, 400],
        "TIME_GENERATED": timeline.default_time["Base_time"],
        "TIME_APPLIED": [timeline.default_time["Base_time"], timeline.default_time["Look_ahead_time_uc"]],
        "TIME_COMMANDED": timeline.default_time["Base_time"],
        "COMMAND_SHED": 0,
        "COMMAND_RESERVE":0,
    }
