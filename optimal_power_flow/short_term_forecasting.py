# Forecasting thread for short term forecasting.
from forecasting.short_term_forecasting import short_term_forecasting_pv, short_term_forecasting_wp, \
    short_term_forecasting_load_ac, short_term_forecasting_load_dc, short_term_forecasting_load_uac, \
    short_term_forecasting_load_udc

import threading
from utils import Logger
from copy import deepcopy
logger = Logger("Short_term_forecasting")
class ForecastingThread(threading.Thread):
    # Thread operation with time control and return value
    def __init__(self, session, Target_time, models):
        threading.Thread.__init__(self)
        self.session = session
        self.Target_time = Target_time
        self.models = models

    def run(self):
        self.models = short_term_forecasting(self.session, self.Target_time, self.models)


def short_term_forecasting(*args):
    session = args[0]
    Target_time = args[1]
    models = deepcopy(args[2])

    if models["PV"]["GEN_STATUS"] > 0:
        pv_profile = short_term_forecasting_pv(session, Target_time)
        models["PV"]["PG"] = round(models["PV"]["PMAX"] * pv_profile)
    else:
        logger.warning("No PV is connected, set to default value 0!")
        models["PV"]["PG"] = 0

    if models["WP"]["GEN_STATUS"] > 0:
        pv_profile = short_term_forecasting_wp(session, Target_time)
        models["WP"]["PG"] = round(models["WP"]["PMAX"] * pv_profile)
    else:
        logger.warning("No WP is connected, set to default value 0!")
        models["WP"]["PG"] = 0

    if models["Load_ac"]["STATUS"] > 0:
        load_ac = short_term_forecasting_load_ac(session, Target_time)
        models["Load_ac"]["PD"] = round(load_ac * models["Load_ac"]["PDMAX"])
    else:
        logger.warning("No critical AC load is connected, set to default value 0!")
        models["Load_ac"]["PD"] = 0

    if models["Load_uac"]["STATUS"] > 0:
        if models["Load_uac"]["STATUS"] > 0:
            load_uac = short_term_forecasting_load_uac(session, Target_time)
            models["Load_uac"]["PD"] = round(load_uac * models["Load_uac"]["PDMAX"])
        else:
            logger.warning("No non-critical AC load is connected, set to default value 0!")
            models["Load_uac"]["PD"] = 0

    if models["Load_dc"]["STATUS"] > 0:
        load_dc = short_term_forecasting_load_dc(session, Target_time)
        models["Load_dc"]["PD"] = round(load_dc * models["Load_dc"]["PDMAX"])
    else:
        logger.warning("No critical DC load is connected, set to default value 0!")
        models["Load_dc"]["PD"] = 0

    if models["Load_udc"]["STATUS"] > 0:
        load_udc = short_term_forecasting_load_udc(session, Target_time)
        models["Load_udc"]["PD"] = round(load_udc * models["Load_udc"]["PDMAX"])
    else:
        logger.warning("No non-critical DC load is connected, set to default value 0!")
        models["Load_udc"]["PD"] = 0

    return models
