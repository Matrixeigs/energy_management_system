# The input information check function for the optimal power flow
# Two types of information will be checked, shown as follows.
# 1) universal model, which contains the connection and topology information within the microgrid parks
# 2) local model, which contains the local sources information

# The following rules are used
# 1) Online status of generators
# 2) Capacity

# Important notice:
# The input check is the oriented from the start-up of the local ems and universal ems

from copy import deepcopy
from configuration.configuration_time_line import default_look_ahead_time_step
from utils import Logger
logger = Logger("Short_term_dispatch_input_check")
from configuration import configuration_default_generators

class input_check_short_term():
    def model_local_check(*args):
        model = deepcopy(args[0]) # The input model

        T_short = default_look_ahead_time_step["Look_ahead_time_opf_time_step"] # The look ahead time step for short term operation
        # 1) The input check of utility grid
        if len(model["UG"]["GEN_STATUS"]) != T_short:
            logger.error("The size of utility grid status is incorrect!")
            logger.info("The status of utility grid has been reset to online!")
            model["UG"]["GEN_STATUS"] = [1]*T_short
        if type(model["UG"]["PMAX"]) is not float or int:
            logger.error("The data format of utility grid capacity is incorrect!")
            try:
                logger.warning("Try to fix the capacity of utility grid")
                model["UG"]["PMAX"] = model["UG"]["PMAX"][0]
            except:
                logger.info("The correction of utility grid capacity failed! Restore it to default value in configuration file!")
                model["UG"]["PMAX"] = configuration_default_generators.default_AC_generator_parameters["PMAX"]
        if type(model["UG"]["PMIN"]) is not float or int:
            logger.error("The data format of utility grid capacity is incorrect!")
            try:
                logger.warning("Try to fix the capacity of utility grid")
                model["UG"]["PMIN"] = model["UG"]["PMIN"][0]
            except:
                logger.info("The correction of utility grid capacity failed! Restore it to default value in configuration file!")
                model["UG"]["PMIN"] = configuration_default_generators.default_AC_generator_parameters["PMIN"]
        if model["UG"]["PMIN"]>model["UG"]["PMAX"]:
            logger.error("The maximal capacity of UG is smaller than the minimal capacity!")
            logger.info("Correct the capacity to its lower boundary!")
            model["UG"]["PMIN"] = model["UG"]["PMAX"]

        # 2) The input check of diesel generator
        if len(model["DG"]["GEN_STATUS"]) != T_short:
            logger.error("The size of diesel generator status is incorrect!")
            logger.info("The status of diesel generator has been reset to online!")
            model["DG"]["GEN_STATUS"] = [1]*T_short
        if type(model["DG"]["PMAX"]) is not float or int:
            logger.error("The data format of diesel generator capacity is incorrect!")
            try:
                logger.warning("Try to fix the capacity of diesel generator")
                model["DG"]["PMAX"] = model["DG"]["PMAX"][0]
            except:
                logger.info("The correction of diesel generator capacity failed! Restore it to default value in configuration file!")
                model["DG"]["PMAX"] = configuration_default_generators.default_AC_generator_parameters["PMAX"]
        if type(model["DG"]["PMIN"]) is not float or int:
            logger.error("The data format of diesel generator capacity is incorrect!")
            try:
                logger.warning("Try to fix the capacity of diesel generator")
                model["DG"]["PMIN"] = model["DG"]["PMIN"][0]
            except:
                logger.info("The correction of diesel generator capacity failed! Restore it to default value in configuration file!")
                model["DG"]["PMIN"] = configuration_default_generators.default_AC_generator_parameters["PMIN"]
        if model["DG"]["PMIN"]>model["DG"]["PMAX"]:
            logger.error("The maximal capacity of UG is smaller than the minimal capacity!")
            model["DG"]["PMIN"] = model["DG"]["PMAX"]

        # 3) The input check of photovoltaic generators
        if len(model["PV"]["NPV"]) != T_short:
            logger.error("The size of photovoltaic generator status is incorrect!")
            logger.info("The status of photovoltaic generator has been reset to online!")
            model["PV"]["NPV"] = [configuration_default_generators.default_RES_generator_parameters["NPV"]] * T_short
        if type(model["PV"]["PMAX"]) is not float or int:
            logger.error("The data format of photovoltaic generator capacity is incorrect!")
            try:
                logger.warning("Try to fix the capacity of photovoltaic generator")
                model["PV"]["PMAX"] = model["PV"]["PMAX"][0]
            except:
                logger.info("The correction of diesel generator capacity failed! Restore it to default value in configuration file!")
                model["PV"]["PMAX"] = configuration_default_generators.default_RES_generator_parameters["PMAX"]
        if type(model["DG"]["PMIN"]) is not float or int:
            logger.error("The data format of diesel generator capacity is incorrect!")
            try:
                logger.warning("Try to fix the capacity of diesel generator")
                model["DG"]["PMIN"] = model["DG"]["PMIN"][0]
            except:
                logger.info("The correction of diesel generator capacity failed! Restore it to default value in configuration file!")
                model["DG"]["PMIN"] = configuration_default_generators.default_AC_generator_parameters["PMIN"]
        if model["DG"]["PMIN"] > model["DG"]["PMAX"]:
            logger.error("The maximal capacity of UG is smaller than the minimal capacity!")
            model["DG"]["PMIN"] = model["DG"]["PMAX"]




