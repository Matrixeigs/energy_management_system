# Setting point tracing function for the optimal power flow
# 1) query middle2short database
# 2) update models of DG status, UG status, Battery SOC and line flows
# 3) if any information is missing, the setting point tracing will not be triggered

from data_management.database_format import middle2short
from configuration.configuration_time_line import default_time


def long2middle_opeartion(*args):
    Target_time = args[0]  # Target time is the start time of scheduling in long-term operation
    model = args[1]  # Solution of the long-term operation
    session = args[2]  # Database session
    delta_T = default_time["Time_step_opf"]
    compress_rate = int(default_time["Time_step_ed"] / default_time["Time_step_opf"])
    add_len = int(default_time["Look_ahead_time_ed"] / delta_T)  # Amount of data should be added

    for i in range(add_len):  # Add the set-pointed repeatly
        if session.query(middle2short).filter(middle2short.TIME_STAMP == Target_time + i * delta_T).count() == 0:
            blank_row = middle2short(TIME_STAMP=Target_time + i * delta_T,
                                    DG_STATUS=model["DG"]["COMMAND_START_UP"][int(i / compress_rate)],
                                    DG_PG=model["DG"]["COMMAND_PG"][int(i / compress_rate)],
                                    DG_QG=0,
                                    UG_STATUS=model["UG"]["COMMAND_START_UP"][int(i / compress_rate)],
                                    UG_PG=model["DG"]["COMMAND_PG"][int(i / compress_rate)],
                                    UG_QG=0,
                                    BIC_PG=model["BIC"]["COMMAND_DC2AC"][int(i / compress_rate)] -
                                           model["BIC"]["COMMAND_AC2DC"][int(i / compress_rate)],
                                    BIC_QG=0,
                                    BAT_PG=model["ESS"]["COMMAND_PG"][int(i / compress_rate)],
                                    BAT_SOC=model["ESS"]["SOC"][int(i / compress_rate)],
                                    PMG=model["PMG"][int(i / compress_rate)],
                                    V_DC=0,
                                    PV_CURT=model["PV"]["COMMAND_CURT"][int(i / compress_rate)],
                                    WP_CURT=model["WP"]["COMMAND_CURT"][int(i / compress_rate)],
                                    AC_SHED=model["Load_ac"]["COMMAND_SHED"][int(i / compress_rate)],
                                    UAC_SHED=model["Load_uac"]["COMMAND_SHED"][int(i / compress_rate)],
                                    DC_SHED=model["Load_dc"]["COMMAND_SHED"][int(i / compress_rate)],
                                    UDC_SHED=model["Load_udc"]["COMMAND_SHED"][int(i / compress_rate)], )
            session.add(blank_row)
            session.commit()
        else:
            row = session.query(middle2short).filter(middle2short.TIME_STAMP == Target_time + i * delta_T).first()
            # Update the founded rows
            row.TIME_STAMP = Target_time + i * delta_T,
            row.DG_STATUS = model["DG"]["COMMAND_START_UP"][int(i / compress_rate)],
            row.DG_PG = model["DG"]["COMMAND_PG"][int(i / compress_rate)],
            row.DG_QG = 0,
            row.UG_STATUS = model["UG"]["COMMAND_START_UP"][int(i / compress_rate)],
            row.UG_PG = model["DG"]["COMMAND_PG"][int(i / compress_rate)],
            row.UG_QG = 0,
            row.BIC_PG = model["BIC"]["COMMAND_DC2AC"][int(i / compress_rate)] * model["BIC"]["EFF_DC2AC"] - \
                         model["BIC"]["COMMAND_AC2DC"][
                             int(i / compress_rate)],
            row.BIC_QG = 0,
            row.BAT_PG = model["ESS"]["COMMAND_PG"][int(i / compress_rate)],
            row.BAT_SOC = model["ESS"]["SOC"][int(i / compress_rate)],
            row.PMG = model["PMG"][int(i / compress_rate)],
            row.V_DC = 0,
            row.PV_CURT = model["PV"]["COMMAND_CURT"][int(i / compress_rate)],
            row.WP_CURT = model["WP"]["COMMAND_CURT"][int(i / compress_rate)],
            row.AC_SHED = model["Load_ac"]["COMMAND_SHED"][int(i / compress_rate)],
            row.UAC_SHED = model["Load_uac"]["COMMAND_SHED"][int(i / compress_rate)],
            row.DC_SHED = model["Load_dc"]["COMMAND_SHED"][int(i / compress_rate)],
            row.UDC_SHED = model["Load_udc"]["COMMAND_SHED"][int(i / compress_rate)]

            session.commit()