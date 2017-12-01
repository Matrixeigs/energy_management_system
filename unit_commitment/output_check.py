# Output check procedure for optimal power flow
# The following rules are used to test the feasiblity of output
# 1) Active power balancing of on AC bus
# 2) Reactive power balancing of on DC bus

from copy import deepcopy
from configuration.configuration_time_line import default_look_ahead_time_step
from utils import Logger

logger = Logger("Long_term_dispatch_output_check")
from configuration.configuration_eps import default_eps


def output_local_check(*args):
    model = args[0]  # local ems models
    T = default_look_ahead_time_step["Look_ahead_time_uc_time_step"]  # The look ahead time step of optimal power flow
    if model["success"] is True:
        for i in range(T):
            if model["UG"]["COMMAND_PG"][i] + model["DG"]["COMMAND_PG"][i] - model["BIC"]["COMMAND_AC2DC"][i] + \
                    model["BIC"][
                        "COMMAND_DC2AC"][i] * model["BIC"]["EFF_DC2AC"] - model["Load_ac"]["PD"][i] - \
                    model["Load_uac"]["PD"][i] >= \
                    default_eps["ED"] or model["UG"]["COMMAND_PG"][i] + model["DG"]["COMMAND_PG"][i] - \
                    model["BIC"]["COMMAND_AC2DC"][i] + model["BIC"][
                "COMMAND_DC2AC"][i] * model["BIC"]["EFF_DC2AC"] - model["Load_ac"]["PD"][i] - model["Load_uac"]["PD"][
                i] <= \
                    -default_eps["ED"]:
                logger.error("The obtained solution can not meet AC bus power requirement!")
                logger.info(
                    model["UG"]["COMMAND_PG"][i] + model["DG"]["COMMAND_PG"][i] - model["BIC"]["COMMAND_AC2DC"][i] +
                    model["BIC"][
                        "COMMAND_DC2AC"][i] * model["BIC"]["EFF_DC2AC"] - model["Load_ac"]["PD"][i] -
                    model["Load_uac"]["PD"][i])

            if model["ESS"]["COMMAND_PG"][i] + model["BIC"]["COMMAND_AC2DC"][i] * model["BIC"]["EFF_DC2AC"] - \
                    model["BIC"]["COMMAND_DC2AC"][i] - model["Load_dc"]["PD"][i] - model["Load_udc"]["PD"][i] + \
                    model["PV"][
                        "PG"][i] + \
                    model["WP"]["PG"][i] - model["PMG"][i] >= default_eps["ED"] or model["ESS"]["COMMAND_PG"][i] + \
                    model["BIC"]["COMMAND_AC2DC"][i] * model["BIC"]["EFF_DC2AC"] - \
                    model["BIC"]["COMMAND_DC2AC"][i] - model["Load_dc"]["PD"][i] - model["Load_udc"]["PD"][i] + \
                    model["PV"]["PG"][i] + model["WP"]["PG"][i] - model["PMG"][i] <= -default_eps["ED"]:
                logger.error("The obtained solution can not meet DC bus power requirement!")
                logger.info(
                    model["ESS"]["COMMAND_PG"][i] + model["BIC"]["COMMAND_AC2DC"][i] * model["BIC"]["EFF_DC2AC"] -
                    model["BIC"]["COMMAND_DC2AC"][i] - model["Load_dc"]["PD"][i] - model["Load_udc"]["PD"][i] +
                    model["PV"]["PG"][i] + \
                    model["WP"]["PG"][i] - model["PMG"][i])

            if model["BIC"]["COMMAND_AC2DC"][i] * model["BIC"]["COMMAND_DC2AC"][i] is not 0:
                logger.error("There exits bi-directional power flow on BIC!")
    else:
        logger.error("The obtained solution results in load shedding or renewable energy resource shedding!")
        for i in range(T):
            logger.info(
                model["UG"]["COMMAND_PG"][i] + model["DG"]["COMMAND_PG"][i] - model["BIC"]["COMMAND_AC2DC"][i] + model["BIC"][
                    "COMMAND_DC2AC"][i] * model["BIC"]["EFF_DC2AC"] - model["Load_ac"]["PD"][i] - model["Load_uac"]["PD"][i] +
                model["Load_ac"]["COMMAND_SHED"][i] + model["Load_uac"]["COMMAND_SHED"][i])

            logger.info(model["ESS"]["COMMAND_PG"][i] + model["BIC"]["COMMAND_AC2DC"][i] * model["BIC"]["EFF_DC2AC"] - \
                        model["BIC"]["COMMAND_DC2AC"][i] - model["Load_dc"]["PD"][i] - model["Load_udc"]["PD"][i] + model["PV"][
                            "PG"][i] + \
                        model["WP"]["PG"][i] - model["PMG"][i] - model["PV"]["COMMAND_CURT"][i] - model["WP"]["COMMAND_CURT"][i] +
                        model["Load_dc"]["COMMAND_SHED"][i] + model["Load_udc"]["COMMAND_SHED"][i])

            logger.info(model["BIC"]["COMMAND_AC2DC"][i] * model["BIC"]["COMMAND_DC2AC"][i])

    return model
