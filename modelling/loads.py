# Loads modelling in universal energy management system
# Generally, there are two types of loads in the UEMS
import configuration.configuration_default_load as default_parameters

Load_AC = \
    {
        "AREA": default_parameters.default_Load_AC["AREA"],
        "STATUS": default_parameters.default_Load_AC["STATUS"],
        # The generation status, >0 means avalible, otherwise, unavaliable
        "PD": default_parameters.default_Load_AC["PD"],
        "QD": default_parameters.default_Load_AC["QD"],
        "PF": default_parameters.default_Load_AC["PF"],
        "PDMAX": default_parameters.default_Load_AC["PDMAX"],
        "PDMIN": default_parameters.default_Load_AC["PDMIN"],
        "FLEX": default_parameters.default_Load_AC["FLEX"],  # 0, load is undispatchable;1, load is dispatchable
        "APF": default_parameters.default_Load_AC["APF"],
        "MODEL": default_parameters.default_Load_AC["MODEL"],
        # 0, load is discrete dispatchable;1, load is contineously dispatchable
        "COST_MODEL": default_parameters.default_Load_AC["COST_MODEL"],
        "NCOST": default_parameters.default_Load_AC["NCOST"],
        "COST": default_parameters.default_Load_AC["COST"],
        "TIME_GENERATED": default_parameters.default_Load_AC["TIME_GENERATED"],
        "TIME_APPLIED": default_parameters.default_Load_AC["TIME_APPLIED"],
        "TIME_COMMANDED": default_parameters.default_Load_AC["TIME_COMMANDED"],
        "COMMAND_SHED": default_parameters.default_Load_AC["COMMAND_SHED"],
        "COMMAND_RESERVE": default_parameters.default_Load_AC["COMMAND_RESERVE"],
    }

Load_DC = \
    {
        "AREA": default_parameters.default_Load_DC["AREA"],
        "STATUS": default_parameters.default_Load_DC["STATUS"],
        # The generation status, >0 means avalible, otherwise, unavaliable
        "PD": default_parameters.default_Load_DC["PD"],
        "PF": default_parameters.default_Load_DC["PF"],
        "PDMAX": default_parameters.default_Load_DC["PDMAX"],
        "PDMIN": default_parameters.default_Load_DC["PDMIN"],
        "FLEX": default_parameters.default_Load_DC["FLEX"],  # 0, load is undispatchable;1, load is dispatchable
        "APF": default_parameters.default_Load_DC["APF"],
        "MODEL": default_parameters.default_Load_DC["MODEL"],
        # 0, load is discrete dispatchable;1, load is contineously dispatchable
        "COST_MODEL": default_parameters.default_Load_DC["COST_MODEL"],
        "NCOST": default_parameters.default_Load_DC["NCOST"],
        "COST": default_parameters.default_Load_DC["COST"],
        "TIME_GENERATED": default_parameters.default_Load_DC["TIME_GENERATED"],
        "TIME_APPLIED": default_parameters.default_Load_DC["TIME_APPLIED"],
        "TIME_COMMANDED": default_parameters.default_Load_DC["TIME_COMMANDED"],
        "COMMAND_SHED": default_parameters.default_Load_DC["COMMAND_SHED"],
        "COMMAND_RESERVE": default_parameters.default_Load_DC["COMMAND_RESERVE"],
    }
