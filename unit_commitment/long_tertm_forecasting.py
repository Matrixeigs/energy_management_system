""" The long_term term forcasting for universal energy management system.
\author: Tianyang Zhao
\mail: zhaoty@ntu.edu.sg
\date: 21/Sep/2017
This part of work follows LiSong's work.

"""
from forecasting.long_term_forecasting import long_term_forecasting_pv, long_term_forecasting_wp, \
    long_term_forecasting_load_ac, long_term_forecasting_load_dc, long_term_forecasting_load_uac, \
    long_term_forecasting_load_udc
from configuration.configuration_time_line import default_look_ahead_time_step

import threading
from utils import Logger

logger = Logger("Long_term_forecasting")


class ForecastingThread(threading.Thread):
    # Thread operation with time control and return value
    def __init__(self, session, Target_time, models):
        threading.Thread.__init__(self)
        self.session = session
        self.Target_time = Target_time
        self.models = models

    def run(self):
        self.models = long_term_forecasting(self.session, self.Target_time, self.models)


def long_term_forecasting(*args):
    session = args[0]
    Target_time = args[1]
    models = args[2]
    T = default_look_ahead_time_step["Look_ahead_time_ed_time_step"]
    if models["PV"]["GEN_STATUS"] > 0:
        pv_profile = long_term_forecasting_pv(session, Target_time)
        models["PV"]["PG"] = []
        for i in range(T):
            models["PV"]["PG"].append(round(models["PV"]["PMAX"] * pv_profile[i]))
    else:
        logger.warning("No PV is connected, set to default value 0!")
        models["PV"]["PG"] = []
        for i in range(T):
            models["PV"]["PG"].append(round(models["PV"]["PMAX"] * 0))

    if models["WP"]["GEN_STATUS"] > 0:
        wp_profile = long_term_forecasting_wp(session, Target_time)
        models["WP"]["PG"] = []
        for i in range(T):
            models["WP"]["PG"].append(round(models["WP"]["PMAX"] * wp_profile[i]))
    else:
        logger.warning("No WP is connected, set to default value 0!")
        models["WP"]["PG"] = []
        for i in range(T):
            models["WP"]["PG"].append(round(models["WP"]["PMAX"] * 0))

    if models["Load_ac"]["STATUS"] > 0:
        load_ac = long_term_forecasting_load_ac(session, Target_time)
        models["Load_ac"]["PD"] = []
        for i in range(T):
            models["Load_ac"]["PD"].append(round(load_ac[i] * models["Load_ac"]["PDMAX"]))
    else:
        logger.warning("No critical AC load is connected, set to default value 0!")
        models["Load_ac"]["PD"] = []
        for i in range(T):
            models["Load_ac"]["PD"].append(round(0 * models["Load_ac"]["PDMAX"]))

    if models["Load_uac"]["STATUS"] > 0:
        if models["Load_uac"]["STATUS"] > 0:
            load_uac = long_term_forecasting_load_uac(session, Target_time)
            models["Load_uac"]["PD"] = []
            for i in range(T):
                models["Load_uac"]["PD"].append(round(load_uac[i] * models["Load_uac"]["PDMAX"]))
        else:
            logger.warning("No non-critical AC load is connected, set to default value 0!")
            models["Load_uac"]["PD"] = []
            for i in range(T):
                models["Load_uac"]["PD"].append(round(0 * models["Load_uac"]["PDMAX"]))

    if models["Load_dc"]["STATUS"] > 0:
        load_dc = long_term_forecasting_load_dc(session, Target_time)
        models["Load_dc"]["PD"] = []
        for i in range(T):
            models["Load_dc"]["PD"].append(round(load_dc[i] * models["Load_dc"]["PDMAX"]))
    else:
        logger.warning("No critical DC load is connected, set to default value 0!")
        models["Load_dc"]["PD"] = []
        for i in range(T):
            models["Load_dc"]["PD"].append(round(0 * models["Load_dc"]["PDMAX"]))

    if models["Load_udc"]["STATUS"] > 0:
        load_udc = long_term_forecasting_load_udc(session, Target_time)
        models["Load_udc"]["PD"] = []
        for i in range(T):
            models["Load_udc"]["PD"].append(round(load_udc[i] * models["Load_udc"]["PDMAX"]))
    else:
        logger.warning("No non-critical DC load is connected, set to default value 0!")
        models["Load_udc"]["PD"] = []
        for i in range(T):
            models["Load_udc"]["PD"].append(round(0 * models["Load_udc"]["PDMAX"]))

    return models
