""" History data management for weather station
For incomplete information, most recent data will be used.
"""
# Generate long-term profile for the load
from configuration.configuration_database import local_load_database,local_history_database

from data_management.database_format import db_load_profile,hourly_history_data,half_hourly_history_data,five_minutes_history_data,one_minute_history_data
from sqlalchemy import create_engine  # Import database
from sqlalchemy.orm import sessionmaker

def run():
    db_str = local_load_database["db_str"]
    engine = create_engine(db_str, echo=False)
    Session = sessionmaker(bind=engine)
    session = Session()

    db_str_target = local_history_database["db_str"]
    engine_target = create_engine(db_str_target, echo=False)
    Session_target = sessionmaker(bind=engine_target)
    session_target = Session_target()

    AC_PD = session.query(db_load_profile.Electricity).filter(db_load_profile.TIME_STAMP >= 0).all()
    NAC_PD = session.query(db_load_profile.HVACFan).filter(db_load_profile.TIME_STAMP >= 0).all()
    DC_PD = session.query(db_load_profile.HVAC_electricity).filter(db_load_profile.TIME_STAMP >= 0).all()
    UDC_PD = session.query(db_load_profile.Misc).filter(db_load_profile.TIME_STAMP >= 0).all()

    AC_PD_max = max(AC_PD)
    NAC_PD_max = max(NAC_PD)
    DC_PD_max = max(DC_PD)
    UDC_PD_max = max(UDC_PD)

    T = len(AC_PD)
    AC_PD_normalized = [0]*T
    NAC_PD_normalized = [0]*T
    DC_PD_normalized = [0]*T
    UDC_PD_normalized = [0]*T

    for i in range(T): # One year's data
        AC_PD_normalized[i] = AC_PD[i][0]/AC_PD_max[0]
        NAC_PD_normalized[i] = NAC_PD[i][0]/NAC_PD_max[0]
        DC_PD_normalized[i] = DC_PD[i][0]/DC_PD_max[0]
        UDC_PD_normalized[i] = UDC_PD[i][0]/UDC_PD_max[0]
    #
    #     if session_target.query(hourly_history_data).filter(hourly_history_data.TIME_STAMP == i).count() == 0:
    #         default_result = hourly_history_data (TIME_STAMP=i,
    #              AC_PD=AC_PD_normalized[i],
    #              AC_QD=0,
    #              NAC_PD=NAC_PD_normalized[i],
    #              NAC_QD=0,
    #              DC_PD=DC_PD_normalized[i],
    #              NDC_PD=UDC_PD_normalized[i],
    #              PV_PG=0,
    #              WP_PG=0,)
    #         session_target.add(default_result)
    #         session_target.commit()
    #     else:
    #         row = session_target.query(hourly_history_data).filter(hourly_history_data.TIME_STAMP == i).first()
    #         row.AC_PD = AC_PD_normalized[i]
    #         row.NAC_PD = NAC_PD_normalized[i]
    #         row.DC_PD = DC_PD_normalized[i]
    #         row.NDC_PD = UDC_PD_normalized[i]
    #         session_target.commit()
    #
    #     print(i)

    # for i in range(2*T): # half year's data
    #     if session_target.query(half_hourly_history_data).filter(half_hourly_history_data.TIME_STAMP == i).count() == 0:
    #         default_result = half_hourly_history_data (TIME_STAMP=i,
    #              AC_PD=AC_PD_normalized[int(i/2)],
    #              AC_QD=0,
    #              NAC_PD=NAC_PD_normalized[int(i/2)],
    #              NAC_QD=0,
    #              DC_PD=DC_PD_normalized[int(i/2)],
    #              NDC_PD=UDC_PD_normalized[int(i/2)],
    #              PV_PG=0,
    #              WP_PG=0,)
    #         session_target.add(default_result)
    #         session_target.commit()
    #     else:
    #         row = session_target.query(half_hourly_history_data).filter(half_hourly_history_data.TIME_STAMP == i).first()
    #         row.AC_PD = AC_PD_normalized[int(i/2)]
    #         row.NAC_PD = NAC_PD_normalized[int(i/2)]
    #         row.DC_PD = DC_PD_normalized[int(i/2)]
    #         row.NDC_PD = UDC_PD_normalized[int(i/2)]
    #         session_target.commit()
    #
    #     print(i)
    # for i in range(12 * T):  # five minutes' data
    #     if session_target.query(five_minutes_history_data).filter(five_minutes_history_data.TIME_STAMP == i).count() == 0:
    #         default_result = five_minutes_history_data(TIME_STAMP=i,
    #                                                    AC_PD = AC_PD_normalized[int(i/12)],
    #                                                    AC_QD = 0,
    #                                                    NAC_PD = NAC_PD_normalized[int(i/12)],
    #                                                    NAC_QD = 0,
    #                                                    DC_PD = DC_PD_normalized[int(i/12)],
    #                                                    NDC_PD = UDC_PD_normalized[int(i/12)],
    #                                                    PV_PG = 0,
    #                                                    WP_PG = 0, )
    #         session_target.add(default_result)
    #         session_target.commit()
    #     else:
    #         row = session_target.query(five_minutes_history_data).filter(five_minutes_history_data.TIME_STAMP == i).first()
    #         row.AC_PD = AC_PD_normalized[int(i/12)]
    #         row.NAC_PD = NAC_PD_normalized[int(i/12)]
    #         row.DC_PD = DC_PD_normalized[int(i/12)]
    #         row.NDC_PD = UDC_PD_normalized[int(i/12)]
    #
    #         session_target.commit()
    #
    #     print(i)

    for i in range(60 * T):  # one minute's data
        if session_target.query(one_minute_history_data).filter(one_minute_history_data.TIME_STAMP == i).count() == 0:
            default_result = one_minute_history_data(TIME_STAMP=i,
                                                       AC_PD = AC_PD_normalized[int(i/60)],
                                                       AC_QD = 0,
                                                       NAC_PD = NAC_PD_normalized[int(i/60)],
                                                       NAC_QD = 0,
                                                       DC_PD = DC_PD_normalized[int(i/60)],
                                                       NDC_PD = UDC_PD_normalized[int(i/60)],
                                                       PV_PG = 0,
                                                       WP_PG = 0, )
            session_target.add(default_result)
            session_target.commit()
        else:
            row = session_target.query(one_minute_history_data).filter(one_minute_history_data.TIME_STAMP == i).first()
            row.AC_PD = AC_PD_normalized[int(i/60)]
            row.NAC_PD = NAC_PD_normalized[int(i/60)]
            row.DC_PD = DC_PD_normalized[int(i/60)]
            row.NDC_PD = UDC_PD_normalized[int(i/60)]

            session_target.commit()

        print(i)





if __name__ == "__main__":
    ## Start the main process of local energy management system
    run()
