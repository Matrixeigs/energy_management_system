""" The long_term term forcasting for universal energy management system.
\author: Tianyang Zhao
\mail: zhaoty@ntu.edu.sg
\date: 21/Sep/2017
This part of work follows LiSong's work.

"""
from forecasting.long_term_forecasting import long_term_forecasting_pv_history, long_term_forecasting_wp_history, \
    long_term_forecasting_load_ac_history, long_term_forecasting_load_dc_history, long_term_forecasting_load_uac_history, \
    long_term_forecasting_load_udc_history
from configuration.configuration_time_line import default_look_ahead_time_step

import threading
from utils import Logger
from copy import deepcopy
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
    models = deepcopy(args[2])
    T = default_look_ahead_time_step["Look_ahead_time_uc_time_step"] # The look ahead horizon of unit commitment
    models["PV"]["PG"] = []
    models["WP"]["PG"] = []
    models["Load_ac"]["PD"] = []
    models["Load_uac"]["PD"] = []
    models["Load_dc"]["PD"] = []
    models["Load_udc"]["PD"] = []
    pv_profile = long_term_forecasting_pv_history(session, Target_time)
    wp_profile = long_term_forecasting_wp_history(session, Target_time)
    load_ac = long_term_forecasting_load_ac_history(session, Target_time)
    load_uac = long_term_forecasting_load_uac_history(session, Target_time)
    load_dc = long_term_forecasting_load_dc_history(session, Target_time)
    load_udc = long_term_forecasting_load_udc_history(session, Target_time)

    for i in range(T):
        # Update the forecasting result of PV
        if models["PV"]["NPV"][i] > 0:
            models["PV"]["PG"].append(round(models["PV"]["PMAX"][i] * pv_profile[i]))
        else:
            models["PV"]["PG"].append(0)

        if models["WP"]["NWP"][i] > 0:
            models["WP"]["PG"].append(round(models["WP"]["PMAX"][i] * wp_profile[i]))
        else:
            models["WP"]["PG"].append(0)

        if models["Load_ac"]["STATUS"][i] > 0:
            models["Load_ac"]["PD"].append(round(load_ac[i] * models["Load_ac"]["PDMAX"]))
        else:
            models["Load_ac"]["PD"].append(0)

        if models["Load_uac"]["STATUS"][i] > 0:
            models["Load_uac"]["PD"].append(round(load_uac[i] * models["Load_uac"]["PDMAX"]))
        else:
            models["Load_uac"]["PD"].append(0)

        if models["Load_dc"]["STATUS"][i] > 0:
            models["Load_dc"]["PD"].append(round(load_dc[i] * models["Load_dc"]["PDMAX"]))
        else:
            models["Load_dc"]["PD"].append(0)

        if models["Load_udc"]["STATUS"][i] > 0:
            models["Load_udc"]["PD"].append(round(load_udc[i] * models["Load_udc"]["PDMAX"]))
        else:
            models["Load_udc"]["PD"].append(0)

    return models
