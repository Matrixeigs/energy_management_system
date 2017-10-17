# Short_term forecasting for local energy management system
# Include the pv forecasting, wp forecasting,
# In this forecasting system, the tensor flow will be deployed and used.
# The training

from data_management.database_format import db_short_term_forecasting
import random


def blank_forecasting_result(*args):
    Target_time = args[0]
    default_result = db_short_term_forecasting \
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


def short_term_forecasting_pv(*args):
    # Short term forecasting for photovoltaic
    session = args[0]
    Target_Time = args[1]

    if session.query(db_short_term_forecasting).filter(
                    db_short_term_forecasting.TIME_STAMP == Target_Time).count() == 0:
        blank_row = blank_forecasting_result(Target_Time)
        session.add(blank_row)
        session.commit()

    PV_PG = random.random()
    row = session.query(db_short_term_forecasting).filter_by(TIME_STAMP=Target_Time).first()
    row.PV_PG = PV_PG
    session.commit()

    return PV_PG


def short_term_forecasting_wp(*args):
    # Short term forecasting for wind power
    session = args[0]
    Target_Time = args[1]

    if session.query(db_short_term_forecasting).filter(
                    db_short_term_forecasting.TIME_STAMP == Target_Time).count() == 0:
        blank_row = blank_forecasting_result(Target_Time)
        session.add(blank_row)
        session.commit()

    WP_PG = random.random()
    row = session.query(db_short_term_forecasting).filter_by(TIME_STAMP=Target_Time).first()
    row.WP_PG = WP_PG
    session.commit()

    return WP_PG


def short_term_forecasting_load_ac(*args):
    # Short term forecasting for critical AC load
    session = args[0]
    Target_Time = args[1]

    if session.query(db_short_term_forecasting).filter(
                    db_short_term_forecasting.TIME_STAMP == Target_Time).count() == 0:
        blank_row = blank_forecasting_result(Target_Time)
        session.add(blank_row)
        session.commit()

    AC_PD = random.random()
    row = session.query(db_short_term_forecasting).filter_by(TIME_STAMP=Target_Time).first()
    row.AC_PD = AC_PD
    session.commit()

    return AC_PD


def short_term_forecasting_load_uac(*args):
    # Short term forecasting for non-critical AC load
    session = args[0]
    Target_Time = args[1]

    if session.query(db_short_term_forecasting).filter(
                    db_short_term_forecasting.TIME_STAMP == Target_Time).count() == 0:
        blank_row = blank_forecasting_result(Target_Time)
        session.add(blank_row)
        session.commit()

    UAC_PD = random.random()
    row = session.query(db_short_term_forecasting).filter_by(TIME_STAMP=Target_Time).first()
    row.UAC_PD = UAC_PD
    session.commit()

    return UAC_PD


def short_term_forecasting_load_dc(*args):
    # Short term forecasting for critical DC load
    session = args[0]
    Target_Time = args[1]

    if session.query(db_short_term_forecasting).filter(
                    db_short_term_forecasting.TIME_STAMP == Target_Time).count() == 0:
        blank_row = blank_forecasting_result(Target_Time)
        session.add(blank_row)
        session.commit()

    DC_PD = random.random()
    row = session.query(db_short_term_forecasting).filter_by(TIME_STAMP=Target_Time).first()
    row.DC_PD = DC_PD
    session.commit()

    return DC_PD


def short_term_forecasting_load_udc(*args):
    # Short term forecasting for non-critical DC load
    session = args[0]
    Target_Time = args[1]

    if session.query(db_short_term_forecasting).filter(
                    db_short_term_forecasting.TIME_STAMP == Target_Time).count() == 0:
        blank_row = blank_forecasting_result(Target_Time)
        session.add(blank_row)
        session.commit()

    UDC_PD = random.random()
    row = session.query(db_short_term_forecasting).filter_by(TIME_STAMP=Target_Time).first()
    row.UDC_PD = UDC_PD
    session.commit()

    return UDC_PD

