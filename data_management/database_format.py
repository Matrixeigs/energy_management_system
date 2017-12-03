## The database format for universal energy management system.
## As there are three processes in the the operation, there are three tablets for all processes.
## For each equipment, the operation status in specific operation process is recorded as well.
## The following parameters are required to be recorded in the database.
## The naming of the database follow the following rules.
## 1)G represents the injection.
## 2)D represents the absorption.
## 3)AC represents for the alternative current.
## 4)DC represents for the direct current.
## 5)U represents for the uncritical.
## 6)P represents for the active power.
## 7)Q represents for the reactive power.

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, FLOAT, INTEGER, DATETIME, BINARY

Base = declarative_base()


class db_long_term_forecasting(Base):
    # Long-term forecasting results.(For unit commitment.)
    __tablename__ = 'long_term_forecasting'

    # The unique and primary key in long term forecasting.
    TIME_STAMP = Column(INTEGER, primary_key=True)

    # Load group.
    AC_PD = Column(FLOAT)
    AC_QD = Column(FLOAT)
    UAC_PD = Column(FLOAT)
    UAC_QD = Column(FLOAT)
    DC_PD = Column(FLOAT)
    UDC_PD = Column(FLOAT)

    # Renewable energy group.
    PV_PG = Column(FLOAT)
    WP_PG = Column(FLOAT)

    # Price information.
    PRICE = Column(FLOAT)


class db_mid_term_forecasting(Base):
    # Mid-term forecasting results.(For economic dispatch.)
    __tablename__ = 'mid_term_forecasting'

    # The unique and primary key in long term forecasting.
    TIME_STAMP = Column(INTEGER, primary_key=True)

    # Load group.
    AC_PD = Column(FLOAT)
    AC_QD = Column(FLOAT)
    UAC_PD = Column(FLOAT)
    UAC_QD = Column(FLOAT)
    DC_PD = Column(FLOAT)
    UDC_PD = Column(FLOAT)

    # Renewable energy group.
    PV_PG = Column(FLOAT)
    WP_PG = Column(FLOAT)

    # Price information.
    PRICE = Column(FLOAT)


class db_short_term_forecasting(Base):
    # Short-term forecasting results.(For optimal power flow.)
    __tablename__ = 'short_term_forecasting'

    # The unique and primary key in long term forecasting.
    TIME_STAMP = Column(INTEGER, primary_key=True)

    # Load group.
    AC_PD = Column(FLOAT)
    AC_QD = Column(FLOAT)
    UAC_PD = Column(FLOAT)
    UAC_QD = Column(FLOAT)
    DC_PD = Column(FLOAT)
    UDC_PD = Column(FLOAT)

    # Renewable energy group.
    PV_PG = Column(FLOAT)
    WP_PG = Column(FLOAT)

    # Price information.
    PRICE = Column(FLOAT)


class db_unit_commitment(Base):
    # Long_term operation database format.
    __tablename__ = 'long_term_operation'
    TIME_STAMP = Column(INTEGER, primary_key=True)  # The primary and unique key in the database.
    # Forecasting results group.
    # Load group.
    AC_PD = Column(INTEGER)
    AC_QD = Column(INTEGER)
    UAC_PD = Column(INTEGER)
    UAC_QD = Column(INTEGER)
    DC_PD = Column(INTEGER)
    UDC_PD = Column(INTEGER)
    # Renewable energy group.
    PV_PG = Column(INTEGER)
    WP_PG = Column(INTEGER)
    PRICE = Column(FLOAT)
    # Schedulable sources group.
    # AC side
    # Generations
    DG_STATUS = Column(BINARY)
    DG_PG = Column(INTEGER)
    DG_QG = Column(INTEGER)
    # Utility grid.
    UG_STATUS = Column(BINARY)
    UG_PG = Column(INTEGER)
    UG_QG = Column(INTEGER)
    # BIC
    BIC_PG = Column(INTEGER)
    BIC_QG = Column(INTEGER)
    # DC side
    # Battery.
    BAT_PG = Column(INTEGER)
    BAT_SOC = Column(FLOAT)
    # The universal energy management settings. If it is a local version, these parameters will not be generated.
    PMG = Column(INTEGER)
    V_DC = Column(FLOAT)
    # Emergency operation
    # Renewable energy curtailment.
    PV_CURT = Column(INTEGER)
    WP_CURT = Column(INTEGER)
    # Load shedding.
    AC_SHED = Column(INTEGER)
    UAC_SHED = Column(INTEGER)
    DC_SHED = Column(INTEGER)
    UDC_SHED = Column(INTEGER)


class db_economic_dispatch(Base):
    # Mid_term operation database format.
    __tablename__ = 'mid_term_operation'
    TIME_STAMP = Column(INTEGER, primary_key=True)  # The primary and unique key in the database.
    # Forecasting results group.
    # Load group.
    AC_PD = Column(INTEGER)
    AC_QD = Column(INTEGER)
    UAC_PD = Column(INTEGER)
    UAC_QD = Column(INTEGER)
    DC_PD = Column(INTEGER)
    UDC_PD = Column(INTEGER)
    # Renewable energy group.
    PV_PG = Column(INTEGER)
    WP_PG = Column(INTEGER)
    PRICE = Column(FLOAT)
    # Schedulable sources group.
    # AC side
    # Generations
    DG_STATUS = Column(BINARY)
    DG_PG = Column(INTEGER)
    DG_QG = Column(INTEGER)
    # Utility grid.
    UG_STATUS = Column(BINARY)
    UG_PG = Column(INTEGER)
    UG_QG = Column(INTEGER)
    # BIC
    BIC_PG = Column(INTEGER)
    BIC_QG = Column(INTEGER)
    # DC side
    # Battery.
    BAT_PG = Column(INTEGER)
    BAT_SOC = Column(FLOAT)
    # The universal energy management settings. If it is a local version, these parameters will not be generated.
    PMG = Column(INTEGER)
    V_DC = Column(FLOAT)
    # Emergency operation
    # Renewable energy curtailment.
    PV_CURT = Column(INTEGER)
    WP_CURT = Column(INTEGER)
    # Load shedding.
    AC_SHED = Column(INTEGER)
    UAC_SHED = Column(INTEGER)
    DC_SHED = Column(INTEGER)
    UDC_SHED = Column(INTEGER)


class db_optimal_power_flow(Base):
    # The database format of optimal power flow.
    __tablename__ = 'short_term_operation'

    TIME_STAMP = Column(INTEGER, primary_key=True)  # The primary and unique key in the database.
    # Forecasting results group.
    # Load group.
    AC_PD = Column(INTEGER)
    AC_QD = Column(INTEGER)
    UAC_PD = Column(INTEGER)
    UAC_QD = Column(INTEGER)
    DC_PD = Column(INTEGER)
    UDC_PD = Column(INTEGER)
    # Renewable energy group.
    PV_PG = Column(INTEGER)
    WP_PG = Column(INTEGER)
    # Schedulable sources group.
    # AC side
    # Generations
    DG_STATUS = Column(BINARY)
    DG_PG = Column(INTEGER)
    DG_QG = Column(INTEGER)
    # Utility grid.
    UG_STATUS = Column(BINARY)
    UG_PG = Column(INTEGER)
    UG_QG = Column(INTEGER)
    # BIC
    BIC_PG = Column(INTEGER)
    BIC_QG = Column(INTEGER)
    # DC side
    # Battery.
    BAT_PG = Column(INTEGER)
    BAT_SOC = Column(FLOAT)
    # The universal energy management settings. If it is a local version, these parameters will not be generated.
    PMG = Column(INTEGER)
    V_DC = Column(FLOAT)
    # Emergency operation
    # Renewable energy curtailment.
    PV_CURT = Column(INTEGER)
    WP_CURT = Column(INTEGER)
    # Load shedding.
    AC_SHED = Column(INTEGER)
    UAC_SHED = Column(INTEGER)
    DC_SHED = Column(INTEGER)
    UDC_SHED = Column(INTEGER)

class db_load_profile(Base):
    # Load profile format
    __tablename__ = 'USA_FL_NASA'

    # The data is obtained from NASA.
    TIME_STAMP = Column(INTEGER, primary_key=True)

    Electricity = Column(FLOAT)
    Gas = Column(FLOAT)

    Heating_electricity = Column(FLOAT)
    Heating_gas = Column(FLOAT)
    Cooling = Column(FLOAT)

    HVACFan = Column(FLOAT)
    HVAC_electricity = Column(FLOAT)
    Fans = Column(FLOAT)

    InteriorLights = Column(FLOAT)
    ExteriorLights = Column(FLOAT)
    InteriorEquipment = Column(FLOAT)

    Misc = Column(FLOAT)
    WaterSystems = Column(FLOAT)

class weather_station(Base):
    # Weather station data format
    __tablename__ = 'ISSData'

    # The data is obtained from NASA.
    ReceiverRecID = Column(INTEGER, primary_key=True)

    ChannelIndex = Column(FLOAT)
    RecDateTime = Column(DATETIME)

    TempOut = Column(INTEGER)
    HiTempOut = Column(INTEGER)
    LowTempOut = Column(INTEGER)

    HumOut = Column(INTEGER)
    WindSpeed = Column(INTEGER)
    ScalerAvgWindDir = Column(INTEGER)

    HiWindSpeed = Column(INTEGER)
    HiWindDir = Column(INTEGER)
    DominantDir = Column(INTEGER)
    DewPoint = Column(INTEGER)

    LowWindChill = Column(INTEGER)
    HeatIndex = Column(INTEGER)

    THSWIndex = Column(INTEGER)
    RainCollectorType = Column(INTEGER)
    RainCollectorInc = Column(INTEGER)
    TotalRainClicks = Column(INTEGER)
    HiRainRate = Column(INTEGER)
    ET = Column(INTEGER)
    UV = Column(INTEGER)
    HiUV = Column(INTEGER)
    SolarRad = Column(INTEGER)
    HiSolarRad = Column(INTEGER)
    IntervalIndex = Column(INTEGER)

class hourly_history_data(Base):
    # hourly data
    __tablename__ = 'hourly_data'
    TIME_STAMP = Column(INTEGER, primary_key=True)
    AC_PD = Column(FLOAT)
    AC_QD = Column(FLOAT)
    NAC_PD = Column(FLOAT)
    NAC_QD = Column(FLOAT)
    DC_PD = Column(FLOAT)
    NDC_PD = Column(FLOAT)
    PV_PG = Column(FLOAT)
    WP_PG = Column(FLOAT)

class half_hourly_history_data(Base):
    # half hourly data
    __tablename__ = 'half_hour_data'
    TIME_STAMP = Column(INTEGER, primary_key=True)
    AC_PD = Column(FLOAT)
    AC_QD = Column(FLOAT)
    NAC_PD = Column(FLOAT)
    NAC_QD = Column(FLOAT)
    DC_PD = Column(FLOAT)
    NDC_PD = Column(FLOAT)
    PV_PG = Column(FLOAT)
    WP_PG = Column(FLOAT)

class five_minutes_history_data(Base):
    # five minutes data
    __tablename__ = 'five_minutes_data'
    TIME_STAMP = Column(INTEGER, primary_key=True)
    AC_PD = Column(FLOAT)
    AC_QD = Column(FLOAT)
    NAC_PD = Column(FLOAT)
    NAC_QD = Column(FLOAT)
    DC_PD = Column(FLOAT)
    NDC_PD = Column(FLOAT)
    PV_PG = Column(FLOAT)
    WP_PG = Column(FLOAT)

class one_minute_history_data(Base):
    # one minute data
    __tablename__ = 'one_minute_data'
    TIME_STAMP = Column(INTEGER, primary_key=True)
    AC_PD = Column(FLOAT)
    AC_QD = Column(FLOAT)
    NAC_PD = Column(FLOAT)
    NAC_QD = Column(FLOAT)
    DC_PD = Column(FLOAT)
    NDC_PD = Column(FLOAT)
    PV_PG = Column(FLOAT)
    WP_PG = Column(FLOAT)

class long2middle(Base):
    # convert long-term operation schedule to middle-term schedule
    __tablename__ = 'long2middle'
    TIME_STAMP = Column(INTEGER, primary_key=True)
    DG_STATUS = Column(INTEGER)
    DG_PG = Column(INTEGER)
    DG_QG = Column(INTEGER)
    UG_STATUS = Column(INTEGER)
    UG_PG = Column(INTEGER)
    UG_QG = Column(INTEGER)
    BIC_PG = Column(INTEGER)
    BIC_QG = Column(INTEGER)
    BAT_PG = Column(INTEGER)
    BAT_SOC = Column(FLOAT)
    PMG = Column(INTEGER)
    V_DC = Column(FLOAT)
    PV_CURT = Column(INTEGER)
    WP_CURT = Column(INTEGER)
    AC_SHED = Column(INTEGER)
    UAC_SHED = Column(INTEGER)
    DC_SHED = Column(INTEGER)
    UDC_SHED = Column(INTEGER)

class middle2short(Base):
    # convert middle-term operation schedule to short-term operation schedule
    __tablename__ = 'middle2short'
    TIME_STAMP = Column(INTEGER, primary_key=True)
    DG_STATUS = Column(INTEGER)
    DG_PG = Column(INTEGER)
    DG_QG = Column(INTEGER)
    UG_STATUS = Column(INTEGER)
    UG_PG = Column(INTEGER)
    UG_QG = Column(INTEGER)
    BIC_PG = Column(INTEGER)
    BIC_QG = Column(INTEGER)
    BAT_PG = Column(INTEGER)
    BAT_SOC = Column(FLOAT)
    PMG = Column(INTEGER)
    V_DC = Column(FLOAT)
    PV_CURT = Column(INTEGER)
    WP_CURT = Column(INTEGER)
    AC_SHED = Column(INTEGER)
    UAC_SHED = Column(INTEGER)
    DC_SHED = Column(INTEGER)
    UDC_SHED = Column(INTEGER)
