# Setting point tracing function for the optimal power flow
# 1) query middle2short database
# 2) update models of DG status, UG status, Battery SOC and line flows
# 3) if any information is missing, the setting point tracing will not be triggered

from data_management.database_format import middle2short
from configuration.configuration_time_line import default_time,default_look_ahead_time_step

def set_points_tracing_opf(*args):
    Target_time = args[0] # Target time is the start time of scheduling in long-term operation
    model = args[2] # Solution of the long-term operation
    session = args[1] # Database session

    delta_T = default_time["Time_step_opf"]
    T = default_look_ahead_time_step["Look_ahead_time_ed_time_step"] #Amount of data should be addedsss

    model["DG"]["COMMAND_START_UP"] = [0] * T
    model["DG"]["COMMAND_PG"] = [0] * T
    model["DG"]["COMMAND_RG"] = [0] * T

    model["UG"]["COMMAND_START_UP"] = [0] * T
    model["UG"]["COMMAND_PG"] = [0] * T
    model["UG"]["COMMAND_RG"] = [0] * T

    model["BIC"]["COMMAND_AC2DC"] = [0] * T
    model["BIC"]["COMMAND_DC2AC"] = [0] * T

    model["ESS"]["COMMAND_PG"] = [0] * T
    model["ESS"]["COMMAND_RG"] = [0] * T
    model["ESS"]["SOC"] = [0] * T

    model["PV"]["COMMAND_CURT"] = [0] * T
    model["WP"]["COMMAND_CURT"] = [0] * T

    model["PMG"] = [0] * T

    model["Load_ac"]["COMMAND_SHED"] = [0] * T
    model["Load_uac"]["COMMAND_SHED"] = [0] * T
    model["Load_dc"]["COMMAND_SHED"] = [0] * T
    model["Load_udc"]["COMMAND_SHED"] = [0] * T

    for i in range(T):
        row = session.query(middle2short).filter(middle2short.TIME_STAMP == Target_time + i * delta_T).count()
        model["DG"]["COMMAND_START_UP"][i] = row.DG_STATUS
        model["DG"]["COMMAND_PG"][i] = row.DG_PG


        model["UG"]["COMMAND_START_UP"][i] = row.UG_STATUS
        model["UG"]["COMMAND_PG"][i] = row.UG_PG

        if row.BIC_PG>0:
            model["BIC"]["COMMAND_AC2DC"][i] = 0
            model["BIC"]["COMMAND_DC2AC"][i] = row.BIC_PG
        else:
            model["BIC"]["COMMAND_AC2DC"][i] = -row.BIC_PG
            model["BIC"]["COMMAND_DC2AC"][i] = 0

        model["ESS"]["COMMAND_PG"][i] = row.BAT_PG

        model["ESS"]["SOC"][i] = row.BAT_SOC

        model["PMG"][i] = row.PMG

        model["PV"]["COMMAND_CURT"][i] = row.PV_CURT
        model["WP"]["COMMAND_CURT"][i] = row.WP_CURT

        model["Load_ac"]["COMMAND_SHED"][i] = row.AC_SHED
        model["Load_uac"]["COMMAND_SHED"][i] = row.UAC_SHED
        model["Load_dc"]["COMMAND_SHED"][i] = row.DC_SHED
        model["Load_udc"]["COMMAND_SHED"][i] = row.UDC_SHED