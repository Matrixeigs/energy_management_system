# Long_term forecasting for local energy management system
# This function can be replaced with other forecasting engining

from data_management.database_format import db_long_term_forecasting
from configuration.configuration_time_line import default_look_ahead_time_step, default_time
import random


def blank_forecasting_result(*args):
    Target_time = args[0]
    default_result = db_long_term_forecasting \
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


def long_term_forecasting_pv(*args):
    # Short term forecasting for photovoltaic
    session = args[0]
    Target_Time = args[1]

    if session.query(db_long_term_forecasting).filter(
                    db_long_term_forecasting.TIME_STAMP == Target_Time).count() == 0:
        # The forecasting result dose not exist, a dynamic forecasting will be triggered!
        for i in range(default_look_ahead_time_step["Look_ahead_time_uc_time_step"]):
            blank_row = blank_forecasting_result(Target_Time + i * default_time["Time_step_uc"])
            session.add(blank_row)
            session.commit()

    PV_PG = []
    for i in range(default_look_ahead_time_step["Look_ahead_time_uc_time_step"]):
        PV_PG.append(random.random())
        try:
            row = session.query(db_long_term_forecasting).filter_by(
                TIME_STAMP=Target_Time + i * default_time["Time_step_uc"]).first()
            row.PV_PG = PV_PG[i]
        except:
            blank_row = blank_forecasting_result(Target_Time + i * default_time["Time_step_uc"])
            session.add(blank_row)
            session.commit()

            row = session.query(db_long_term_forecasting).filter_by(
                TIME_STAMP=Target_Time + i * default_time["Time_step_uc"]).first()
            row.PV_PG = PV_PG[i]

        session.commit()

    return PV_PG


def long_term_forecasting_wp(*args):
    # Short term forecasting for wind power
    session = args[0]
    Target_Time = args[1]

    if session.query(db_long_term_forecasting).filter(
                    db_long_term_forecasting.TIME_STAMP == Target_Time).count() == 0:
        # The forecasting result dose not exist, a dynamic forecasting will be triggered!
        for i in range(default_look_ahead_time_step["Look_ahead_time_uc_time_step"]):
            blank_row = blank_forecasting_result(Target_Time + i * default_time["Time_step_uc"])
            session.add(blank_row)
            session.commit()

    WP_PG = []
    for i in range(default_look_ahead_time_step["Look_ahead_time_uc_time_step"]):
        WP_PG.append(random.random())
        try:
            row = session.query(db_long_term_forecasting).filter_by(
                TIME_STAMP=Target_Time + i * default_time["Time_step_uc"]).first()
            row.WP_PG = WP_PG[i]
        except:
            blank_row = blank_forecasting_result(Target_Time + i * default_time["Time_step_uc"])
            session.add(blank_row)
            session.commit()
            row = session.query(db_long_term_forecasting).filter_by(
                TIME_STAMP=Target_Time + i * default_time["Time_step_uc"]).first()
            row.WP_PG = WP_PG[i]
        session.commit()

    return WP_PG


def long_term_forecasting_load_ac(*args):
    # Short term forecasting for critical AC load
    session = args[0]
    Target_Time = args[1]

    if session.query(db_long_term_forecasting).filter(
                    db_long_term_forecasting.TIME_STAMP == Target_Time).count() == 0:
        # The forecasting result dose not exist, a dynamic forecasting will be triggered!
        for i in range(default_look_ahead_time_step["Look_ahead_time_uc_time_step"]):
            blank_row = blank_forecasting_result(Target_Time + i * default_time["Time_step_ed"])
            session.add(blank_row)
            session.commit()

    AC_PD = []
    for i in range(default_look_ahead_time_step["Look_ahead_time_uc_time_step"]):
        AC_PD.append(random.random())
        try:
            row = session.query(db_long_term_forecasting).filter_by(
                TIME_STAMP=Target_Time + i * default_time["Time_step_uc"]).first()
            row.AC_PD = AC_PD[i]
        except:
            blank_row = blank_forecasting_result(Target_Time + i * default_time["Time_step_ed"])
            session.add(blank_row)
            session.commit()

            row = session.query(db_long_term_forecasting).filter_by(
                TIME_STAMP=Target_Time + i * default_time["Time_step_uc"]).first()
            row.AC_PD = AC_PD[i]

        session.commit()
    return AC_PD


def long_term_forecasting_load_uac(*args):
    # Short term forecasting for non-critical AC load
    session = args[0]
    Target_Time = args[1]

    if session.query(db_long_term_forecasting).filter(
                    db_long_term_forecasting.TIME_STAMP == Target_Time).count() == 0:
        # The forecasting result dose not exist, a dynamic forecasting will be triggered!
        for i in range(default_look_ahead_time_step["Look_ahead_time_uc_time_step"]):
            blank_row = blank_forecasting_result(Target_Time + i * default_time["Time_step_uc"])
            session.add(blank_row)
            session.commit()

    UAC_PD = []
    for i in range(default_look_ahead_time_step["Look_ahead_time_uc_time_step"]):
        UAC_PD.append(random.random())
        try:
            row = session.query(db_long_term_forecasting).filter_by(
                TIME_STAMP=Target_Time + i * default_time["Time_step_uc"]).first()
            row.UAC_PD = UAC_PD[i]
        except:
            blank_row = blank_forecasting_result(Target_Time + i * default_time["Time_step_uc"])
            session.add(blank_row)
            session.commit()

            row = session.query(db_long_term_forecasting).filter_by(
                TIME_STAMP=Target_Time + i * default_time["Time_step_uc"]).first()
            row.UAC_PD = UAC_PD[i]

        session.commit()

    return UAC_PD


def long_term_forecasting_load_dc(*args):
    # Short term forecasting for critical DC load
    session = args[0]
    Target_Time = args[1]

    if session.query(db_long_term_forecasting).filter(
                    db_long_term_forecasting.TIME_STAMP == Target_Time).count() == 0:
        # The forecasting result dose not exist, a dynamic forecasting will be triggered!
        for i in range(default_look_ahead_time_step["Look_ahead_time_uc_time_step"]):
            blank_row = blank_forecasting_result(Target_Time + i * default_time["Time_step_uc"])
            session.add(blank_row)
            session.commit()

    DC_PD = []
    for i in range(default_look_ahead_time_step["Look_ahead_time_uc_time_step"]):
        DC_PD.append(random.random())
        try:
            row = session.query(db_long_term_forecasting).filter_by(
                TIME_STAMP=Target_Time + i * default_time["Time_step_uc"]).first()
            row.DC_PD = DC_PD[i]
        except:
            blank_row = blank_forecasting_result(Target_Time + i * default_time["Time_step_uc"])
            session.add(blank_row)
            session.commit()

            row = session.query(db_long_term_forecasting).filter_by(
                TIME_STAMP=Target_Time + i * default_time["Time_step_uc"]).first()
            row.DC_PD = DC_PD[i]

        session.commit()


    return DC_PD


def long_term_forecasting_load_udc(*args):
    # Short term forecasting for non-critical DC load
    session = args[0]
    Target_Time = args[1]

    if session.query(db_long_term_forecasting).filter(
                    db_long_term_forecasting.TIME_STAMP == Target_Time).count() == 0:
        # The forecasting result dose not exist, a dynamic forecasting will be triggered!
        for i in range(default_look_ahead_time_step["Look_ahead_time_uc_time_step"]):
            blank_row = blank_forecasting_result(Target_Time + i * default_time["Time_step_uc"])
            session.add(blank_row)
            session.commit()

    UDC_PD = []
    for i in range(default_look_ahead_time_step["Look_ahead_time_uc_time_step"]):
        UDC_PD.append(random.random())
        try:
            row = session.query(db_long_term_forecasting).filter_by(
                TIME_STAMP=Target_Time + i * default_time["Time_step_uc"]).first()
            row.UDC_PD = UDC_PD[i]
        except:
            blank_row = blank_forecasting_result(Target_Time + i * default_time["Time_step_uc"])
            session.add(blank_row)
            session.commit()
            row = session.query(db_long_term_forecasting).filter_by(
                TIME_STAMP=Target_Time + i * default_time["Time_step_uc"]).first()
            row.UDC_PD = UDC_PD[i]

        session.commit()

    return UDC_PD
