# The configuration of time line information
# All the time information is measured by the second(1s).


##############The basic time configuration of different operating process#####
default_time = \
    {   "Base_time":1506182400,
        "Time_step_uc": 1800,  # The time step of unit committment
        "Time_step_ed": 300,  # The time step of economic dispatch
        "Time_step_opf": 60,  # The time step of optimal power flow
        "Look_ahead_time_uc": 24 * 3600,  # The look ahead time of unit committment
        "Look_ahead_time_ed": 3600,  # The look ahead time of economic dispatch
        "Look_ahead_time_opf": 60,
    }
##The start time of each process
default_start_time = \
    {
        "Start_time_uc": default_time["Time_step_uc"],
        "Start_time_ed": default_time["Time_step_ed"],
        "Start_time_opf": default_time["Time_step_opf"],
    }
# The look ahead time step of each process
# Number of decision making within each decision process
default_look_ahead_time_step = \
    {
        "Look_ahead_time_uc_time_step": round(default_time["Look_ahead_time_uc"] / default_time["Time_step_uc"]),
        "Look_ahead_time_ed_time_step": round(
            default_time["Look_ahead_time_ed"] / default_time["Time_step_ed"]),
        "Look_ahead_time_opf_time_step": round(default_time["Look_ahead_time_opf"] / default_time["Time_step_opf"]),
    }
# The deadline of each process
default_dead_line_time = \
    {
        "Gate_closure_uc": default_start_time["Start_time_uc"] - default_start_time["Start_time_ed"],
        "Gate_closure_ed": default_start_time["Start_time_ed"] - default_start_time["Start_time_opf"],
        "Gate_closure_opf": 5,
    }
