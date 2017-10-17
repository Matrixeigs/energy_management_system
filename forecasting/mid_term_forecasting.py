# Mid_term forecasting for local energy management system
from data_management.database_format import db_mid_term_forecasting
from configuration.configuration_time_line import default_look_ahead_time_step, default_time
import random


def blank_forecasting_result(*args):
    Target_time = args[0]
    default_result = db_mid_term_forecasting \
        (TIME_STAMP=Target_time,
         AC_PD=0,
         AC_QD=0,
         UAC_PD=0,
         UAC_QD=0,
         DC_PD=0,
         UDC_PD=0,
         PV_PG=0,
         WP_PG=0,
         PRICE=0, )
    return default_result


def middle_term_forecasting_pv(*args):
    # Short term forecasting for photovoltaic
    session = args[0]
    Target_Time = args[1]

    if session.query(db_mid_term_forecasting).filter(
                    db_mid_term_forecasting.TIME_STAMP == Target_Time).count() == 0:
        # The forecasting result dose not exist, a dynamic forecasting will be triggered!
        for i in range(default_look_ahead_time_step["Look_ahead_time_ed_time_step"]):
            blank_row = blank_forecasting_result(Target_Time + i * default_time["Time_step_ed"])
            session.add(blank_row)
            session.commit()

    PV_PG = []
    for i in range(default_look_ahead_time_step["Look_ahead_time_ed_time_step"]):
        PV_PG.append(random.random())
        row = session.query(db_mid_term_forecasting).filter_by(
            TIME_STAMP=Target_Time + i * default_time["Time_step_ed"]).first()
        row.PV_PG = PV_PG[i]
        session.commit()

    return PV_PG


def middle_term_forecasting_wp(*args):
    # Short term forecasting for wind power
    session = args[0]
    Target_Time = args[1]

    if session.query(db_mid_term_forecasting).filter(
                    db_mid_term_forecasting.TIME_STAMP == Target_Time).count() == 0:
        # The forecasting result dose not exist, a dynamic forecasting will be triggered!
        for i in range(default_look_ahead_time_step["Look_ahead_time_ed_time_step"]):
            blank_row = blank_forecasting_result(Target_Time + i * default_time["Time_step_ed"])
            session.add(blank_row)
            session.commit()

    WP_PG = []
    for i in range(default_look_ahead_time_step["Look_ahead_time_ed_time_step"]):
        WP_PG.append(random.random())
        row = session.query(db_mid_term_forecasting).filter_by(
            TIME_STAMP=Target_Time + i * default_time["Time_step_ed"]).first()
        row.PV_PG = WP_PG[i]
        session.commit()

    return WP_PG


def middle_term_forecasting_load_ac(*args):
    # Short term forecasting for critical AC load
    session = args[0]
    Target_Time = args[1]

    if session.query(db_mid_term_forecasting).filter(
                    db_mid_term_forecasting.TIME_STAMP == Target_Time).count() == 0:
        # The forecasting result dose not exist, a dynamic forecasting will be triggered!
        for i in range(default_look_ahead_time_step["Look_ahead_time_ed_time_step"]):
            blank_row = blank_forecasting_result(Target_Time + i * default_time["Time_step_ed"])
            session.add(blank_row)
            session.commit()

    AC_PD = []
    for i in range(default_look_ahead_time_step["Look_ahead_time_ed_time_step"]):
        AC_PD.append(random.random())
        row = session.query(db_mid_term_forecasting).filter_by(
            TIME_STAMP=Target_Time + i * default_time["Time_step_ed"]).first()
        row.PV_PG = AC_PD[i]
        session.commit()
    return AC_PD


def middle_term_forecasting_load_uac(*args):
    # Short term forecasting for non-critical AC load
    session = args[0]
    Target_Time = args[1]

    if session.query(db_mid_term_forecasting).filter(
                    db_mid_term_forecasting.TIME_STAMP == Target_Time).count() == 0:
        # The forecasting result dose not exist, a dynamic forecasting will be triggered!
        for i in range(default_look_ahead_time_step["Look_ahead_time_ed_time_step"]):
            blank_row = blank_forecasting_result(Target_Time + i * default_time["Time_step_ed"])
            session.add(blank_row)
            session.commit()

    UAC_PD = []
    for i in range(default_look_ahead_time_step["Look_ahead_time_ed_time_step"]):
        UAC_PD.append(random.random())
        row = session.query(db_mid_term_forecasting).filter_by(
            TIME_STAMP=Target_Time + i * default_time["Time_step_ed"]).first()
        row.PV_PG = UAC_PD[i]
        session.commit()

    return UAC_PD


def middle_term_forecasting_load_dc(*args):
    # Short term forecasting for critical DC load
    session = args[0]
    Target_Time = args[1]

    if session.query(db_mid_term_forecasting).filter(
                    db_mid_term_forecasting.TIME_STAMP == Target_Time).count() == 0:
        # The forecasting result dose not exist, a dynamic forecasting will be triggered!
        for i in range(default_look_ahead_time_step["Look_ahead_time_ed_time_step"]):
            blank_row = blank_forecasting_result(Target_Time + i * default_time["Time_step_ed"])
            session.add(blank_row)
            session.commit()

    DC_PD = []
    for i in range(default_look_ahead_time_step["Look_ahead_time_ed_time_step"]):
        DC_PD.append(random.random())
        row = session.query(db_mid_term_forecasting).filter_by(
            TIME_STAMP=Target_Time + i * default_time["Time_step_ed"]).first()
        row.PV_PG = DC_PD[i]
        session.commit()


    return DC_PD


def middle_term_forecasting_load_udc(*args):
    # Short term forecasting for non-critical DC load
    session = args[0]
    Target_Time = args[1]

    if session.query(db_mid_term_forecasting).filter(
                    db_mid_term_forecasting.TIME_STAMP == Target_Time).count() == 0:
        # The forecasting result dose not exist, a dynamic forecasting will be triggered!
        for i in range(default_look_ahead_time_step["Look_ahead_time_ed_time_step"]):
            blank_row = blank_forecasting_result(Target_Time + i * default_time["Time_step_ed"])
            session.add(blank_row)
            session.commit()

    UDC_PD = []
    for i in range(default_look_ahead_time_step["Look_ahead_time_ed_time_step"]):
        UDC_PD.append(random.random())
        row = session.query(db_mid_term_forecasting).filter_by(
            TIME_STAMP=Target_Time + i * default_time["Time_step_ed"]).first()
        row.PV_PG = UDC_PD[i]
        session.commit()

    return UDC_PD
