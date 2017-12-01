# Output check procedure for optimal power flow
# The following rules are used to test the feasiblity of output
# 1) Active power balancing of on AC bus
# 2) Reactive power balancing of on DC bus

from copy import deepcopy
from configuration.configuration_time_line import default_look_ahead_time_step
from utils import Logger

logger = Logger("Short_term_dispatch_output_check")
from configuration.configuration_eps import default_eps


def output_local_check(*args):
    model = args[0]  # local ems models
    T = default_look_ahead_time_step["Look_ahead_time_opf_time_step"]  # The look ahead time step of optimal power flow
    if model["success"] is True:
        if model["UG"]["COMMAND_PG"] + model["DG"]["COMMAND_PG"] - model["BIC"]["COMMAND_AC2DC"] + model["BIC"][
            "COMMAND_DC2AC"] * model["BIC"]["EFF_DC2AC"] - model["Load_ac"]["PD"] - model["Load_uac"]["PD"] >= \
                default_eps[
                    "OPF"] or model["UG"]["COMMAND_PG"] + model["DG"]["COMMAND_PG"] - model["BIC"]["COMMAND_AC2DC"] + \
                model["BIC"][
                    "COMMAND_DC2AC"] * model["BIC"]["EFF_DC2AC"] - model["Load_ac"]["PD"] - model["Load_uac"]["PD"] <= - \
        default_eps[
            "OPF"]:
            logger.error("The obtained solution can not meet AC bus power requirement!")
            logger.info(model["UG"]["COMMAND_PG"] + model["DG"]["COMMAND_PG"] - model["BIC"]["COMMAND_AC2DC"] + model["BIC"]["COMMAND_DC2AC"] * model["BIC"]["EFF_DC2AC"] - model["Load_ac"]["PD"] - model["Load_uac"]["PD"])

        if model["ESS"]["COMMAND_PG"] + model["BIC"]["COMMAND_AC2DC"] * model["BIC"]["EFF_DC2AC"] - \
                model["BIC"]["COMMAND_DC2AC"] - model["Load_dc"]["PD"] - model["Load_udc"]["PD"] + model["PV"]["PG"] + \
                model["WP"]["PG"] - model["PMG"] >= default_eps["OPF"] or model["ESS"]["COMMAND_PG"] + model["BIC"][
            "COMMAND_AC2DC"] * model["BIC"]["EFF_DC2AC"] - model["BIC"]["COMMAND_DC2AC"] - model["Load_dc"]["PD"] - \
                model["Load_udc"]["PD"] + model["PV"]["PG"] + model["WP"]["PG"] - model["PMG"] <= -default_eps["OPF"]:
            logger.error("The obtained solution can not meet DC bus power requirement!")
            logger.info(model["ESS"]["COMMAND_PG"] + model["BIC"]["COMMAND_AC2DC"] * model["BIC"]["EFF_DC2AC"] - \
                        model["BIC"]["COMMAND_DC2AC"] - model["Load_dc"]["PD"] - model["Load_udc"]["PD"] + model["PV"][
                            "PG"] + \
                        model["WP"]["PG"] - model["PMG"])

        if model["BIC"]["COMMAND_AC2DC"] * model["BIC"]["COMMAND_DC2AC"] is not 0:
            logger.error("There exits bi-directional power flow on BIC!")
    else:
        logger.error("The obtained solution results in load shedding or renewable energy resource shedding!")

        logger.info(
            model["UG"]["COMMAND_PG"] + model["DG"]["COMMAND_PG"] - model["BIC"]["COMMAND_AC2DC"] + model["BIC"][
                "COMMAND_DC2AC"] * model["BIC"]["EFF_DC2AC"] - model["Load_ac"]["PD"] - model["Load_uac"]["PD"] +
            model["Load_ac"]["COMMAND_SHED"] + model["Load_uac"]["COMMAND_SHED"])

        logger.info(model["ESS"]["COMMAND_PG"] + model["BIC"]["COMMAND_AC2DC"] * model["BIC"]["EFF_DC2AC"] - \
                    model["BIC"]["COMMAND_DC2AC"] - model["Load_dc"]["PD"] - model["Load_udc"]["PD"] + model["PV"][
                        "PG"] + \
                    model["WP"]["PG"] - model["PMG"] - model["PV"]["COMMAND_CURT"] - model["WP"]["COMMAND_CURT"] +
                    model["Load_dc"]["COMMAND_SHED"] + model["Load_udc"]["COMMAND_SHED"])

        logger.info(model["BIC"]["COMMAND_AC2DC"] * model["BIC"]["COMMAND_DC2AC"])

    return model
