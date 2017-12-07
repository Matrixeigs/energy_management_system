#Information models of energy storage system models
#The following types of ESSs are included:
#1) Battery energy storage system
#2) Thermal energy storage system
#3) The modelling includes static information, measre
import configuration.configuration_default_ess as default_parameters
############################1) Battery energy storage system ###############
BESS =\
    {
        "AREA": default_parameters.BESS["AREA"],
        "CAP": default_parameters.BESS["CAP"],
        "STATUS": default_parameters.BESS["STATUS"],
        "PMAX_DIS": default_parameters.BESS["PMAX_DIS"],
        "PMAX_CH": default_parameters.BESS["PMAX_CH"],
        "EFF_DIS":default_parameters.BESS["EFF_DIS"],
        "EFF_CH":default_parameters.BESS["EFF_CH"],
        "SOC_MAX":default_parameters.BESS["SOC_MAX"],
        "SOC_MIN":default_parameters.BESS["SOC_MIN"],
        "SOC":default_parameters.BESS["SOC"],
        "PG": default_parameters.BESS["PG"],
        "RG": default_parameters.BESS["RG"],
        "COST_MODEL":default_parameters.BESS["COST_MODEL"],
        "NCOST_DIS":default_parameters.BESS["NCOST_DIS"],
        "COST_DIS":default_parameters.BESS["COST_DIS"],
        "NCOST_CH":default_parameters.BESS["NCOST_CH"],
        "COST_CH":default_parameters.BESS["COST_CH"],
        "TIME_GENERATED": default_parameters.BESS["TIME_GENERATED"],
        "TIME_APPLIED": default_parameters.BESS["TIME_APPLIED"],
        "TIME_COMMANDED": default_parameters.BESS["TIME_COMMANDED"],
        "COMMAND_PG":default_parameters.BESS["COMMAND_PG"],
        "COMMAND_RG":default_parameters.BESS["COMMAND_RG"],
    }

# Parameters annoucement:
# AREA: The integration area
