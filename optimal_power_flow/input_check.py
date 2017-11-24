# The input information check function for the optimal power flow
# Two types of information will be checked, shown as follows.
# 1) universal model, which contains the connection and topology information within the microgrid parks
# 2) local model, which contains the local sources information

# The following rules are used
# 1) Online status of generators
# 2)

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
