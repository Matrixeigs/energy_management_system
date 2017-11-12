# The generators set includes the following types of generators:
# 1) AC generators
# 2) DC generators
# 3) Renewable generatos
import configuration.configuration_default_generators as default_parameters

###################### 1) Generators AC set ##########################
Generator_AC = \
    {
        "AREA": default_parameters.default_AC_generator_parameters["AREA"],
        "GEN_STATUS": default_parameters.default_AC_generator_parameters["GEN_STATUS"],
        # The generation status, >0 means avalible, otherwise, unavaliable
        "PG": default_parameters.default_AC_generator_parameters["PG"],
        "QG": default_parameters.default_AC_generator_parameters["QG"],
        "PMAX": default_parameters.default_AC_generator_parameters["PMAX"],
        "PMIN": default_parameters.default_AC_generator_parameters["PMIN"],
        "QMAX": default_parameters.default_AC_generator_parameters["QMAX"],
        "QMIN": default_parameters.default_AC_generator_parameters["QMIN"],
        "SMAX": default_parameters.default_AC_generator_parameters["SMAX"],
        "VG": default_parameters.default_AC_generator_parameters["VG"],
        "RAMP_AGC": default_parameters.default_AC_generator_parameters["RAMP_AGC"],
        "RAMP_10": default_parameters.default_AC_generator_parameters["RAMP_10"],
        "PF_LIMIT": default_parameters.default_AC_generator_parameters["PF_LIMIT"],
        "APF": default_parameters.default_AC_generator_parameters["APF"],  # The droop parameters
        "COST_START_UP": default_parameters.default_AC_generator_parameters["COMMAND_START_UP"],
        "COST_SHUT_DOWN": default_parameters.default_AC_generator_parameters["COST_SHUT_DOWN"],
        "COST_MODEL": default_parameters.default_AC_generator_parameters["COST_MODEL"],
        "NCOST": default_parameters.default_AC_generator_parameters["NCOST"],
        "COST": default_parameters.default_AC_generator_parameters["COST"],
        "TIME_GENERATED": default_parameters.default_AC_generator_parameters["TIME_GENERATED"],
        "TIME_APPLIED": default_parameters.default_AC_generator_parameters["TIME_APPLIED"],
        "TIME_COMMANDED": default_parameters.default_AC_generator_parameters["TIME_COMMANDED"],
        "COMMAND_START_UP": default_parameters.default_AC_generator_parameters["COMMAND_START_UP"],
        "COMMAND_VG": default_parameters.default_AC_generator_parameters["COMMAND_SET_POINT_VG"],
        "COMMAND_PG": default_parameters.default_AC_generator_parameters["COMMAND_SET_POINT_PG"],
        "COMMAND_QG": default_parameters.default_AC_generator_parameters["COMMAND_SET_POINT_QG"],
        "COMMAND_RG": default_parameters.default_AC_generator_parameters["COMMAND_RESERVE"]
    }

###################### 2) Generators DC set ##########################
Generator_DC = \
    {
        "AREA": default_parameters.default_DC_generator_parameters["AREA"],
        "GEN_STATUS": default_parameters.default_DC_generator_parameters["GEN_STATUS"],
    # The generation status, >0 means avalible, otherwise, unavaliable
        "PG": default_parameters.default_DC_generator_parameters["PG"],
        "PMAX": default_parameters.default_DC_generator_parameters["PMAX"],
        "PMIN": default_parameters.default_DC_generator_parameters["PMIN"],
        "VG": default_parameters.default_DC_generator_parameters["VG"],
        "RAMP_AGC": default_parameters.default_DC_generator_parameters["RAMP_AGC"],
        "RAMP_10": default_parameters.default_DC_generator_parameters["RAMP_10"],
        "APF": default_parameters.default_DC_generator_parameters["APF"],  # The droop parameters
        "COST_START_UP": default_parameters.default_DC_generator_parameters["COST_START_UP"],
        "COST_SHUT_DOWN": default_parameters.default_DC_generator_parameters["COST_SHUT_DOWN"],
        "COST_MODEL": default_parameters.default_DC_generator_parameters["COST_MODEL"],
        "NCOST": default_parameters.default_DC_generator_parameters["NCOST"],
        "COST": default_parameters.default_DC_generator_parameters["COST"],
        "TIME_GENERATED": default_parameters.default_DC_generator_parameters["TIME_GENERATED"],
        "TIME_APPLIED": default_parameters.default_DC_generator_parameters["TIME_APPLIED"],
        "TIME_COMMANDED": default_parameters.default_DC_generator_parameters["TIME_COMMANDED"],
        "COMMAND_START_UP": default_parameters.default_DC_generator_parameters["COMMAND_START_UP"],
        "COMMAND_VG": default_parameters.default_DC_generator_parameters["COMMAND_SET_POINT_VG"],
        "COMMAND_PG": default_parameters.default_DC_generator_parameters["COMMAND_SET_POINT_PG"],
        "COMMAND_RG": default_parameters.default_DC_generator_parameters["COMMAND_RESERVE"]
    }

###################### 3) Generators Renewable set ##########################
Generator_RES = \
    {
        "AREA": default_parameters.default_RES_generator_parameters["AREA"],
        "TYPE": default_parameters.default_RES_generator_parameters["TYPE"],  # 1= PV,2=Wind turbine
        "GEN_STATUS": default_parameters.default_RES_generator_parameters["GEN_STATUS"],
    # The generation status, >0 means avalible, otherwise, unavaliable
        "PG": default_parameters.default_RES_generator_parameters["PG"],
        "QG": default_parameters.default_RES_generator_parameters["QG"],
        "PMAX": default_parameters.default_RES_generator_parameters["PMAX"],
        "PMIN": default_parameters.default_RES_generator_parameters["PMIN"],
        "QMAX": default_parameters.default_RES_generator_parameters["QMAX"],
        "QMIN": default_parameters.default_RES_generator_parameters["QMIN"],
        "SMAX": default_parameters.default_RES_generator_parameters["SMAX"],
        "COST": default_parameters.default_RES_generator_parameters["COST"],
        "TIME_GENERATED": default_parameters.default_RES_generator_parameters["TIME_GENERATED"],
        "TIME_APPLIED": default_parameters.default_RES_generator_parameters["TIME_APPLIED"],
        "TIME_COMMANDED": default_parameters.default_RES_generator_parameters["TIME_COMMANDED"],
        "COMMAND_CURT": default_parameters.default_RES_generator_parameters["COMMAND_CURT"],
        "COMMAND_PG": default_parameters.default_RES_generator_parameters["COMMAND_SET_POINT_PG"],
    }
