# Short_term forecasting for local energy management system
# Include the pv forecasting, wp forecasting,
# In this forecasting system, the tensor flow will be deployed and used.
# The training

from data_management.database_format import db_short_term_forecasting,one_minute_history_data
import random
from configuration.configuration_time_line import default_time
from configuration.configuration_database import local_history_database
from sqlalchemy import create_engine, and_  # Import database
from sqlalchemy.orm import sessionmaker


db_str = local_history_database["db_str"]
engine = create_engine(db_str, echo=False)
Session = sessionmaker(bind=engine)
session_source = Session()

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

def short_term_forecasting_pv_history(*args):
    # Short term forecasting for photovoltaic
    session = args[0]
    Target_Time = args[1]

    if session.query(db_short_term_forecasting).filter(
                    db_short_term_forecasting.TIME_STAMP == Target_Time).count() == 0:
        blank_row = blank_forecasting_result(Target_Time)
        session.add(blank_row)
        session.commit()
    row_source = session_source.query(one_minute_history_data).filter_by(
        TIME_STAMP=int((Target_Time - default_time["Base_time"]) / default_time["Time_step_opf"])).first()

    PV_PG = row_source.PV_PG
    row = session.query(db_short_term_forecasting).filter_by(TIME_STAMP=Target_Time).first()
    row.PV_PG = PV_PG
    session.commit()

    return PV_PG


def short_term_forecasting_wp_history(*args):
    # Short term forecasting for wind power
    session = args[0]
    Target_Time = args[1]

    if session.query(db_short_term_forecasting).filter(
                    db_short_term_forecasting.TIME_STAMP == Target_Time).count() == 0:
        blank_row = blank_forecasting_result(Target_Time)
        session.add(blank_row)
        session.commit()

    row_source = session_source.query(one_minute_history_data).filter_by(
        TIME_STAMP=int((Target_Time - default_time["Base_time"]) / default_time["Time_step_opf"])).first()

    WP_PG = row_source.WP_PG
    row = session.query(db_short_term_forecasting).filter_by(TIME_STAMP=Target_Time).first()
    row.WP_PG = WP_PG
    session.commit()

    return WP_PG


def short_term_forecasting_load_ac_history(*args):
    # Short term forecasting for critical AC load
    session = args[0]
    Target_Time = args[1]

    if session.query(db_short_term_forecasting).filter(
                    db_short_term_forecasting.TIME_STAMP == Target_Time).count() == 0:
        blank_row = blank_forecasting_result(Target_Time)
        session.add(blank_row)
        session.commit()

    row_source = session_source.query(one_minute_history_data).filter_by(
        TIME_STAMP=int((Target_Time - default_time["Base_time"]) / default_time["Time_step_opf"])).first()

    AC_PD = row_source.AC_PD
    row = session.query(db_short_term_forecasting).filter_by(TIME_STAMP=Target_Time).first()
    row.AC_PD = AC_PD
    session.commit()

    return AC_PD


def short_term_forecasting_load_uac_history(*args):
    # Short term forecasting for non-critical AC load
    session = args[0]
    Target_Time = args[1]

    if session.query(db_short_term_forecasting).filter(
                    db_short_term_forecasting.TIME_STAMP == Target_Time).count() == 0:
        blank_row = blank_forecasting_result(Target_Time)
        session.add(blank_row)
        session.commit()

    row_source = session_source.query(one_minute_history_data).filter_by(
        TIME_STAMP=int((Target_Time - default_time["Base_time"]) / default_time["Time_step_opf"])).first()

    UAC_PD = row_source.NAC_PD
    row = session.query(db_short_term_forecasting).filter_by(TIME_STAMP=Target_Time).first()
    row.UAC_PD = UAC_PD
    session.commit()

    return UAC_PD


def short_term_forecasting_load_dc_history(*args):
    # Short term forecasting for critical DC load
    session = args[0]
    Target_Time = args[1]

    if session.query(db_short_term_forecasting).filter(
                    db_short_term_forecasting.TIME_STAMP == Target_Time).count() == 0:
        blank_row = blank_forecasting_result(Target_Time)
        session.add(blank_row)
        session.commit()

    row_source = session_source.query(one_minute_history_data).filter_by(
        TIME_STAMP=int((Target_Time - default_time["Base_time"]) / default_time["Time_step_opf"])).first()

    DC_PD= row_source.DC_PD
    row = session.query(db_short_term_forecasting).filter_by(TIME_STAMP=Target_Time).first()
    row.DC_PD = DC_PD
    session.commit()

    return DC_PD


def short_term_forecasting_load_udc_history(*args):
    # Short term forecasting for non-critical DC load
    session = args[0]
    Target_Time = args[1]

    if session.query(db_short_term_forecasting).filter(
                    db_short_term_forecasting.TIME_STAMP == Target_Time).count() == 0:
        blank_row = blank_forecasting_result(Target_Time)
        session.add(blank_row)
        session.commit()

    row_source = session_source.query(one_minute_history_data).filter_by(
        TIME_STAMP=int((Target_Time - default_time["Base_time"]) / default_time["Time_step_opf"])).first()

    UDC_PD = row_source.NDC_PD
    row = session.query(db_short_term_forecasting).filter_by(TIME_STAMP=Target_Time).first()
    row.UDC_PD = UDC_PD
    session.commit()

    return UDC_PD