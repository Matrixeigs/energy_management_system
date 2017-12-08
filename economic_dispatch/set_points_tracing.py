# Setting point tracing function for the economic dispatch in the universal energy management
# 1) query long2middle database
# 2) update models of DG status, UG status, Battery SOC and line flows
# 3) if any information is missing, the setting point tracing will not be triggered
from data_management.database_format import long2middle
from configuration.configuration_time_line import default_time,default_look_ahead_time_step
from copy import deepcopy

def set_points_tracing_ed(*args):
    Target_time = args[0] # Target time is the start time of scheduling in long-term operation
    session = args[1] # Database session
    model = deepcopy(args[2]) # Solution of the long-term operation

    delta_T = default_time["Time_step_ed"]
    T = default_look_ahead_time_step["Look_ahead_time_ed_time_step"] #Amount of data should be addedsss

    model["DG"]["GEN_STATUS"] = [0] * T
    model["DG"]["COMMAND_PG"] = [0] * T
    model["DG"]["COMMAND_RG"] = [0] * T

    model["UG"]["GEN_STATUS"] = [0] * T
    model["UG"]["COMMAND_PG"] = [0] * T
    model["UG"]["COMMAND_RG"] = [0] * T

    model["BIC"]["COMMAND_AC2DC"] = [0] * T
    model["BIC"]["COMMAND_DC2AC"] = [0] * T

    model["ESS"]["COMMAND_PG"] = [0] * T
    model["ESS"]["COMMAND_RG"] = [0] * T
    model["ESS"]["COMMAND_SOC"] = [0] * T

    model["PV"]["COMMAND_CURT"] = [0] * T
    model["WP"]["COMMAND_CURT"] = [0] * T

    model["PMG"] = [0] * T

    model["Load_ac"]["COMMAND_SHED"] = [0] * T
    model["Load_uac"]["COMMAND_SHED"] = [0] * T
    model["Load_dc"]["COMMAND_SHED"] = [0] * T
    model["Load_udc"]["COMMAND_SHED"] = [0] * T
    try:
        for i in range(T):
            row = session.query(long2middle).filter(long2middle.TIME_STAMP == Target_time + i * delta_T).first()
            model["DG"]["GEN_STATUS"][i] = int(row.DG_STATUS)
            model["DG"]["COMMAND_PG"][i] = row.DG_PG

            model["UG"]["GEN_STATUS"][i] = int(row.UG_STATUS)
            model["UG"]["COMMAND_PG"][i] = row.UG_PG

            if row.BIC_PG > 0 :
                model["BIC"]["COMMAND_AC2DC"][i] = 0
                model["BIC"]["COMMAND_DC2AC"][i] = row.BIC_PG
            else:
                model["BIC"]["COMMAND_AC2DC"][i] = -row.BIC_PG
                model["BIC"]["COMMAND_DC2AC"][i] = 0

            model["ESS"]["COMMAND_PG"][i] = row.BAT_PG
            model["ESS"]["COMMAND_SOC"][i] = row.BAT_SOC

            model["PMG"][i] = row.PMG

            model["PV"]["COMMAND_CURT"][i] = row.PV_CURT
            model["WP"]["COMMAND_CURT"][i] = row.WP_CURT

            model["Load_ac"]["COMMAND_SHED"][i] = row.AC_SHED
            model["Load_uac"]["COMMAND_SHED"][i] = row.UAC_SHED
            model["Load_dc"]["COMMAND_SHED"][i] = row.DC_SHED
            model["Load_udc"]["COMMAND_SHED"][i] = row.UDC_SHED

        model["COMMAND_TYPE"] = 1 # This is the set-point tracing

    except: # If any exception happens, it is not operated in set-point tracing method

        model["COMMAND_TYPE"] = 0  # This is not the set-point tracing

    return model

# For the local energy management
# 1) The information should be embedded into the information model of local ems, and should be sent back to the universal ems
# 2) The universal ems considers the set points of utility grid and energy storage system, and makes the scheduling for all EMSs.
