""" History data management for weather station
For incomplete information, most recent data will be used.
"""
# Generate long-term profile for the load
from configuration.configuration_database import local_load_database,local_history_database,weather_station_database

from data_management.database_format import db_load_profile,hourly_history_data,half_hourly_history_data,five_minutes_history_data,one_minute_history_data
from sqlalchemy import create_engine, and_  # Import database
from sqlalchemy.orm import sessionmaker
from data_management.database_format import weather_station

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

    # for i in range(60 * T):  # one minute's data
    #     if session_target.query(one_minute_history_data).filter(one_minute_history_data.TIME_STAMP == i).count() == 0:
    #         default_result = one_minute_history_data(TIME_STAMP=i,
    #                                                    AC_PD = AC_PD_normalized[int(i/60)],
    #                                                    AC_QD = 0,
    #                                                    NAC_PD = NAC_PD_normalized[int(i/60)],
    #                                                    NAC_QD = 0,
    #                                                    DC_PD = DC_PD_normalized[int(i/60)],
    #                                                    NDC_PD = UDC_PD_normalized[int(i/60)],
    #                                                    PV_PG = 0,
    #                                                    WP_PG = 0, )
    #         session_target.add(default_result)
    #         session_target.commit()
    #     else:
    #         row = session_target.query(one_minute_history_data).filter(one_minute_history_data.TIME_STAMP == i).first()
    #         row.AC_PD = AC_PD_normalized[int(i/60)]
    #         row.NAC_PD = NAC_PD_normalized[int(i/60)]
    #         row.DC_PD = DC_PD_normalized[int(i/60)]
    #         row.NDC_PD = UDC_PD_normalized[int(i/60)]
    #
    #         session_target.commit()
    #
    #     print(i)
# 1490025600
# 179999
def pv_history_data():
    import time,datetime

    start_time = "2017-03-21 00:00:00"
    end_time = "2017-07-23 23:59:59"
    test = "2017-03-21 00:00:00"
    db_str = weather_station_database["db_str"]
    engine = create_engine(db_str, echo=False)
    Session = sessionmaker(bind=engine)
    session = Session()
    session_extra = Session()
    # Fulfill the missing data
    start_time_int = time.mktime(time.strptime(start_time,'%Y-%m-%d %H:%M:%S'))
    end_time_int = time.mktime(time.strptime(end_time,'%Y-%m-%d %H:%M:%S'))
    T = int((end_time_int-start_time_int)/60)

    for i in range(T): # From the beginning to the end
        Time_temp = datetime.datetime.fromtimestamp(start_time_int + i*60)
        if session.query(weather_station).filter(weather_station.RecDateTime == Time_temp).count() is 0:
            print("The information is lost at {}".format(Time_temp))

            Time_repair = datetime.datetime.fromtimestamp(start_time_int + (i-1) * 60)

            try:
                row = session_extra.query(weather_station).filter(weather_station.RecDateTime == Time_repair).first()

                row_blank = weather_station(ReceiverRecID = 1,
                                            ChannelIndex = 0,
                                            RecDateTime = Time_temp,
                                            TempOut = row.TempOut,
                                            HiTempOut = row.HiTempOut,
                                            LowTempOut = row.LowTempOut,
                                            HumOut = row.HumOut,
                                            WindSpeed = row.WindSpeed,
                                            ScalerAvgWindDir = row.ScalerAvgWindDir,
                                            HiWindSpeed = row.HiWindSpeed,
                                            HiWindDir = row.HiWindDir,
                                            DominantDir = row.DominantDir,
                                            DewPoint = row.DewPoint,
                                            LowWindChill = row.LowWindChill,
                                            HeatIndex = row.HeatIndex,
                                            THSWIndex = row.THSWIndex,
                                            RainCollectorType = row.RainCollectorType,
                                            RainCollectorInc = row.RainCollectorInc,
                                            TotalRainClicks = row.TotalRainClicks,
                                            HiRainRate = row.HiRainRate,
                                            ET = row.ET,
                                            UV = row.UV,
                                            HiUV = row.HiUV,
                                            SolarRad = row.SolarRad,
                                            HiSolarRad = row.HiSolarRad,
                                            IntervalIndex = row.IntervalIndex,)
                session.add(row_blank)
                session.commit()
            except:
                row_blank = weather_station(ReceiverRecID=1,
                                            ChannelIndex=0,
                                            RecDateTime=Time_temp,
                                            TempOut=0,
                                            HiTempOut=0,
                                            LowTempOut=0,
                                            HumOut=0,
                                            WindSpeed=0,
                                            ScalerAvgWindDir=0,
                                            HiWindSpeed=0,
                                            HiWindDir=0,
                                            DominantDir=0,
                                            DewPoint=0,
                                            LowWindChill=0,
                                            HeatIndex=0,
                                            THSWIndex=0,
                                            RainCollectorType=0,
                                            RainCollectorInc=0,
                                            TotalRainClicks=0,
                                            HiRainRate=0,
                                            ET=0,
                                            UV=0,
                                            HiUV=0,
                                            SolarRad=0,
                                            HiSolarRad=0,
                                            IntervalIndex=0, )
                session.add(row_blank)
                session.commit()

        else:
            # print("The information is complete at {}".format(Time_temp))
            pass


    # pv_data = session.query(weather_station.SolarRad).filter(and_(weather_station.RecDateTime >= start_time, weather_station.RecDateTime <= end_time)).all()
    #
    # T = len(pv_data)

def one_minute_pv():
    import time,datetime
    start_time = "2017-03-21 00:00:00"
    end_time = "2017-07-23 23:59:59"
    start_time_int = time.mktime(time.strptime(start_time,'%Y-%m-%d %H:%M:%S'))

    db_str_target = local_history_database["db_str"]
    engine_target = create_engine(db_str_target, echo=False)
    Session_target = sessionmaker(bind=engine_target)
    session_target = Session_target()

    db_str = weather_station_database["db_str"]
    engine = create_engine(db_str, echo=False)
    Session = sessionmaker(bind=engine)
    session_source = Session()

    pv_source = session_source.query(weather_station.SolarRad).filter(and_(weather_station.RecDateTime >= start_time, weather_station.RecDateTime <= end_time)).all()
    pv_max = 1313
    pv_len = len(pv_source)

    for i in range(8760*60):

        if i < pv_len:
            Time_temp = datetime.datetime.fromtimestamp(start_time_int + i*60)
        else:
            Time_temp = datetime.datetime.fromtimestamp(start_time_int + (i%pv_len)*60)

        row_source = session_source.query(weather_station.SolarRad).filter(weather_station.RecDateTime == Time_temp).first()

        row = session_target.query(one_minute_history_data).filter(one_minute_history_data.TIME_STAMP == i).first()
        if row_source.SolarRad>pv_max:
            row.PV_PG = 1
        else:
            row.PV_PG = row_source.SolarRad/pv_max
        session_target.commit()
        print(i)

def five_minute_pv():
    db_str_target = local_history_database["db_str"]
    engine_target = create_engine(db_str_target, echo=False)
    Session_target = sessionmaker(bind=engine_target)
    session_target = Session_target()

    session_source = Session_target()

    for i in range(8760*12):

        row_source = session_source.query(one_minute_history_data.PV_PG).filter(and_(one_minute_history_data.TIME_STAMP>=i*5,one_minute_history_data.TIME_STAMP<(i+1)*5)).all()

        row = session_target.query(five_minutes_history_data).filter(five_minutes_history_data.TIME_STAMP == i).first()
        temp = 0
        for j in range(5):
            temp += row_source[j][0]

        row.PV_PG = temp/5

        session_target.commit()
        print(i)

def half_hour_pv():
    db_str_target = local_history_database["db_str"]
    engine_target = create_engine(db_str_target, echo=False)
    Session_target = sessionmaker(bind=engine_target)
    session_target = Session_target()

    session_source = Session_target()

    for i in range(8760*2):

        row_source = session_source.query(five_minutes_history_data.PV_PG).filter(and_(five_minutes_history_data.TIME_STAMP>=i*6,five_minutes_history_data.TIME_STAMP<(i+1)*6)).all()

        row = session_target.query(half_hourly_history_data).filter(half_hourly_history_data.TIME_STAMP == i).first()
        temp = 0
        for j in range(6):
            temp += row_source[j][0]

        row.PV_PG = temp/6

        session_target.commit()
        print(i)

def hourly_pv():
    db_str_target = local_history_database["db_str"]
    engine_target = create_engine(db_str_target, echo=False)
    Session_target = sessionmaker(bind=engine_target)
    session_target = Session_target()

    session_source = Session_target()

    for i in range(8760):

        row_source = session_source.query(half_hourly_history_data.PV_PG).filter(and_(half_hourly_history_data.TIME_STAMP>=i*2,half_hourly_history_data.TIME_STAMP<(i+1)*2)).all()

        row = session_target.query(hourly_history_data).filter(hourly_history_data.TIME_STAMP == i).first()
        temp = 0
        for j in range(2):
            temp += row_source[j][0]

        row.PV_PG = temp/2

        session_target.commit()
        print(i)

if __name__ == "__main__":
    ## Start the main process of local energy management system
    # run()
    # pv_history_data()
    # one_minute_pv()
    # five_minute_pv()
    # half_hour_pv()
    hourly_pv()