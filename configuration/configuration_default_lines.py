import configuration.configuration_time_line as timeline

default_Line = \
    {
        "TYPE":2,
        "F_BUS":1,
        "T_BUS":2,
        "BR_R":0.3,
        "BR_X":0.4,
        "BR_B":0,
        "RATE_A":5000,
        "RATE_B":1000,
        "RATE_C":10000,
        "TAP":1,
        "SHIFT":0,
        "STATUS":1,
        "PF":100,
        "QF":0,
        "TIME_GENERATED": timeline.default_time["Base_time"],
        "TIME_APPLIED": [timeline.default_time["Base_time"], timeline.default_time["Look_ahead_time_uc"]],
        "TIME_COMMANDED": timeline.default_time["Base_time"],
        "COMMAND_STATUS":[1],
        "COMMAND_TAP":[1]

    }