# The configuration files of eps values in calculation
default_eps = \
    {
        "OPF": 1,
        "ED": 1,  # The generation status, >0 means avalible, otherwise, unavaliable
        "UC": 2,
        "Penalty_bic":0.01, # The penalty factor for bi-directional power flow
        "Penalty_uc":0.1,
        "Penalty_ed":0.01,
        "Penalty_opf":0.01,
    }