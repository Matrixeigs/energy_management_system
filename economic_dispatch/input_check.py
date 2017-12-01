# The input information check function for the unit committment
# Two types of information will be checked, shown as follows.
# 1) universal model, which contains the connection and topology information within the microgrid parks
# 2) local model, which contains the local sources information

# The following rules are used
# 1) Online status of generators
# 2) Capacity

# Important notice:
# The input check is the oriented from 1） the start-up of the local ems and universal ems
# 2） modelling of each equipment

from copy import deepcopy
from configuration.configuration_time_line import default_look_ahead_time_step
from utils import Logger

logger = Logger("Middle_term_dispatch_input_check")
from configuration import configuration_default_generators, configuration_default_load, configuration_convertors


class input_check_middle_term():
    def model_local_check(*args):
        model = deepcopy(args[0])  # The input model

        T = default_look_ahead_time_step["Look_ahead_time_ed_time_step"]  # The look ahead time step for short term operation
        # 1) The input check of utility grid
        if len(model["UG"]["GEN_STATUS"]) != T:
            logger.error("The size of utility grid status is incorrect!")
            logger.info("The status of utility grid has been reset to online!")
            model["UG"]["GEN_STATUS"] = [1] * T
        if type(model["UG"]["PMAX"]) is not float and type(model["UG"]["PMAX"]) is not int:
            logger.error("The data format of utility grid capacity is incorrect!")
            try:
                logger.warning("Try to fix the capacity of utility grid")
                model["UG"]["PMAX"] = model["UG"]["PMAX"][0]
            except:
                logger.info("The correction of utility grid capacity failed! Restore it to default value in configuration file!")
                model["UG"]["PMAX"] = configuration_default_generators.default_AC_generator_parameters["PMAX"]
        if type(model["UG"]["PMIN"]) is not float and type(model["UG"]["PMIN"]) is not int:
            logger.error("The data format of utility grid capacity is incorrect!")
            try:
                logger.warning("Try to fix the capacity of utility grid")
                model["UG"]["PMIN"] = model["UG"]["PMIN"][0]
            except:
                logger.info("The correction of utility grid capacity failed! Restore it to default value in configuration file!")
                model["UG"]["PMIN"] = configuration_default_generators.default_AC_generator_parameters["PMIN"]
        if model["UG"]["PMIN"] > model["UG"]["PMAX"]:
            logger.error("The maximal capacity of UG is smaller than the minimal capacity!")
            logger.info("Correct the capacity to its lower boundary!")
            model["UG"]["PMIN"] = model["UG"]["PMAX"]
        if model["UG"]["QMIN"] > model["UG"]["QMAX"]:
            logger.error("The maximal reactive power capacity of UG is smaller than the minimal capacity!")
            logger.info("Correct the reactive power capacity to its lower boundary!")
            model["UG"]["QMIN"] = model["UG"]["QMAX"]

        # 2) The input check of diesel generator
        if len(model["DG"]["GEN_STATUS"]) != T:
            logger.error("The size of diesel generator status is incorrect!")
            logger.info("The status of diesel generator has been reset to online!")
            model["DG"]["GEN_STATUS"] = [1] * T
        if type(model["DG"]["PMAX"]) is not float and type(model["DG"]["PMAX"]) is not int:
            logger.error("The data format of diesel generator capacity is incorrect!")
            try:
                logger.warning("Try to fix the capacity of diesel generator")
                model["DG"]["PMAX"] = model["DG"]["PMAX"][0]
            except:
                logger.info(
                    "The correction of diesel generator capacity failed! Restore it to default value in configuration file!")
                model["DG"]["PMAX"] = configuration_default_generators.default_AC_generator_parameters["PMAX"]
        if type(model["DG"]["PMIN"]) is not float and type(model["DG"]["PMIN"]) is not int:
            logger.error("The data format of diesel generator capacity is incorrect!")
            try:
                logger.warning("Try to fix the capacity of diesel generator")
                model["DG"]["PMIN"] = model["DG"]["PMIN"][0]
            except:
                logger.info(
                    "The correction of diesel generator capacity failed! Restore it to default value in configuration file!")
                model["DG"]["PMIN"] = configuration_default_generators.default_AC_generator_parameters["PMIN"]
        if model["DG"]["PMIN"] > model["DG"]["PMAX"]:
            logger.error("The maximal capacity of UG is smaller than the minimal capacity!")
            model["DG"]["PMIN"] = model["DG"]["PMAX"]
        if model["DG"]["QMIN"] > model["DG"]["QMAX"]:
            logger.error("The maximal reactive power capacity of UG is smaller than the minimal capacity!")
            model["DG"]["QMIN"] = model["DG"]["QMAX"]

        # 3) The input check of photovoltaic generators
        if len(model["PV"]["NPV"]) != T:
            logger.error("The size of photovoltaic generator status is incorrect!")
            logger.info("The status of photovoltaic generator has been reset to online!")
            model["PV"]["NPV"] = [configuration_default_generators.default_RES_generator_parameters["PMAX"]] * T
        if type(model["PV"]["PMAX"]) is not list:
            logger.error("The data format of photovoltaic generator capacity is incorrect!")
            try:
                logger.warning("Try to fix the capacity of photovoltaic generator")
                model["PV"]["PMAX"] = [model["PV"]["PMAX"][0]]*T
            except:
                logger.info(
                    "The correction of photovoltaic generator capacity failed! Restore it to default value in configuration file!")
                model["PV"]["PMAX"] = [configuration_default_generators.default_RES_generator_parameters["PMAX"]]*T


        # 4) The input check of wind turbine generators
        if len(model["WP"]["NWP"]) != T:
            logger.error("The size of WP status is incorrect!")
            logger.info("The status of WP has been reset to online!")
            model["WP"]["NPV"] = [configuration_default_generators.default_RES_generator_parameters["PMAX"]] * T
        if type(model["WP"]["PMAX"]) is not list:
            logger.error("The data format of WP capacity is incorrect!")
            try:
                logger.warning("Try to fix the capacity of WP")
                model["WP"]["PMAX"] = [model["WP"]["PMAX"][0]]*T
            except:
                logger.info("The correction of WP capacity failed! Restore it to default value in configuration file!")
                model["WP"]["PMAX"] = [configuration_default_generators.default_RES_generator_parameters["PMAX"]]*T

        # 5) The input check of critical AC load
        if len(model["Load_ac"]["STATUS"]) != T:
            logger.error("The size of critical AC load status is incorrect!")
            logger.info("The status of critical AC load has been reset to default value!")
            model["Load_ac"]["STATUS"] = [configuration_default_load.default_Load_AC["STATUS"]] * T
        if len(model["Load_ac"]["PD"]) != T:
            logger.error("The size of critical AC load profile is incorrect!")
            logger.info("The profile of critical AC load has been reset to default value!")
            model["Load_ac"]["PD"] = [configuration_default_load.default_Load_AC["PD"]] * T
        for i in range(T):
            if model["Load_ac"]["PD"][i] > model["Load_ac"]["STATUS"][i] * model["Load_ac"]["PDMAX"]:
                logger.error("The critical AC load is over current!")
                logger.info("The critical AC load is set to its default value!")
                model["Load_ac"]["PD"][i] = model["Load_ac"]["STATUS"][i] * model["Load_ac"]["PDMAX"]

        # 6) The input check of non-critical AC load
        if len(model["Load_uac"]["STATUS"]) != T:
            logger.error("The size of non-critical AC load status is incorrect!")
            logger.info("The status of non-critical AC load has been reset to default value!")
            model["Load_uac"]["STATUS"] = [configuration_default_load.default_Load_AC["STATUS"]] * T
        if len(model["Load_uac"]["PD"]) != T:
            logger.error("The size of non-critical AC load profile is incorrect!")
            logger.info("The profile of non-critical AC load has been reset to online!")
            model["Load_uac"]["PD"] = [configuration_default_load.default_Load_AC["PD"]] * T
        for i in range(T):
            if model["Load_uac"]["PD"][i] > model["Load_uac"]["STATUS"][i] * model["Load_uac"]["PDMAX"]:
                logger.error("The non-critical AC load is over current!")
                logger.info("The non-critical AC load is set to its default value!")
                model["Load_uac"]["PD"][i] = model["Load_uac"]["STATUS"][i] * model["Load_uac"]["PDMAX"]

        # 7) The input check of critical AC load
        if len(model["Load_dc"]["STATUS"]) != T:
            logger.error("The size of critical DC load status is incorrect!")
            logger.info("The status of critical DC load has been reset to default value!")
            model["Load_dc"]["STATUS"] = [configuration_default_load.default_Load_DC["STATUS"]] * T
        if len(model["Load_dc"]["PD"]) != T:
            logger.error("The size of critical DC load profile is incorrect!")
            logger.info("The profile of critical DC load has been reset to default value!")
            model["Load_dc"]["PD"] = [configuration_default_load.default_Load_DC["PD"]] * T
        for i in range(T):
            if model["Load_dc"]["PD"][i] > model["Load_dc"]["STATUS"][i] * model["Load_dc"]["PDMAX"]:
                logger.error("The critical DC load is over current!")
                logger.info("The critical DC load is set to its default value!")
                model["Load_dc"]["PD"][i] = model["Load_dc"]["STATUS"][i] * model["Load_dc"]["PDMAX"]

        # 8) The input check of non-critical AC load
        if len(model["Load_udc"]["STATUS"]) != T:
            logger.error("The size of non-critical DC load status is incorrect!")
            logger.info("The status of non-critical DC load has been reset to default value!")
            model["Load_udc"]["STATUS"] = [configuration_default_load.default_Load_DC["STATUS"]] * T
        if len(model["Load_udc"]["PD"]) != T:
            logger.error("The size of non-critical DC load profile is incorrect!")
            logger.info("The profile of non-critical DC load has been reset to online!")
            model["Load_udc"]["PD"] = [configuration_default_load.default_Load_DC["PD"]] * T
        for i in range(T):
            if model["Load_udc"]["PD"][i] > model["Load_udc"]["STATUS"][i] * model["Load_udc"]["PDMAX"]:
                logger.error("The non-critical DC load is over current!")
                logger.info("The non-critical DC load is set to its default value!")
                model["Load_udc"]["PD"][i] = model["Load_udc"]["STATUS"][i] * model["Load_udc"]["PDMAX"]

        # 9) The input check for BIC convertors
        if len(model["BIC"]["STATUS"]) != T:
            logger.error("The size of BIC status is incorrect!")
            logger.info("The status of BIC has been reset to default value!")
            model["BIC"]["STATUS"] = [configuration_convertors.BIC["STATUS"]] * T

        # 10) The input check for ESSs
        if len(model["ESS"]["STATUS"]) != T:
            logger.error("The size of ESS status is incorrect!")
            logger.info("The status of ESS has been reset to default value!")
            model["ESS"]["STATUS"] = [configuration_convertors.BIC["STATUS"]] * T

        return model # return the model
    def model_universal_check(*args):
        model = deepcopy(args[0])  # The input model

        T = default_look_ahead_time_step[
            "Look_ahead_time_ed_time_step"]  # The look ahead time step for short term operation
        # 1) The input check of utility grid
        if len(model["UG"]["GEN_STATUS"]) != T:
            logger.error("The size of utility grid status is incorrect!")
            logger.info("The status of utility grid has been reset to online!")
            model["UG"]["GEN_STATUS"] = [1] * T
        if type(model["UG"]["PMAX"]) is not float and type(model["UG"]["PMAX"]) is not int:
            logger.error("The data format of utility grid capacity is incorrect!")
            try:
                logger.warning("Try to fix the capacity of utility grid")
                model["UG"]["PMAX"] = model["UG"]["PMAX"][0]
            except:
                logger.info("The correction of utility grid capacity failed! Restore it to default value in configuration file!")
                model["UG"]["PMAX"] = configuration_default_generators.default_AC_generator_parameters["PMAX"]
        if type(model["UG"]["PMIN"]) is not float and type(model["UG"]["PMIN"]) is not int:
            logger.error("The data format of utility grid capacity is incorrect!")
            try:
                logger.warning("Try to fix the capacity of utility grid")
                model["UG"]["PMIN"] = model["UG"]["PMIN"][0]
            except:
                logger.info("The correction of utility grid capacity failed! Restore it to default value in configuration file!")
                model["UG"]["PMIN"] = configuration_default_generators.default_AC_generator_parameters["PMIN"]
        if model["UG"]["PMIN"] > model["UG"]["PMAX"]:
            logger.error("The maximal capacity of UG is smaller than the minimal capacity!")
            logger.info("Correct the capacity to its lower boundary!")
            model["UG"]["PMIN"] = model["UG"]["PMAX"]
        if model["UG"]["QMIN"] > model["UG"]["QMAX"]:
            logger.error("The maximal reactive power capacity of UG is smaller than the minimal capacity!")
            logger.info("Correct the reactive power capacity to its lower boundary!")
            model["UG"]["QMIN"] = model["UG"]["QMAX"]

        # 2) The input check of diesel generator
        if len(model["DG"]["GEN_STATUS"]) != T:
            logger.error("The size of diesel generator status is incorrect!")
            logger.info("The status of diesel generator has been reset to online!")
            model["DG"]["GEN_STATUS"] = [1] * T
        if type(model["DG"]["PMAX"]) is not float and type(model["DG"]["PMAX"]) is not int:
            logger.error("The data format of diesel generator capacity is incorrect!")
            try:
                logger.warning("Try to fix the capacity of diesel generator")
                model["DG"]["PMAX"] = model["DG"]["PMAX"][0]
            except:
                logger.info(
                    "The correction of diesel generator capacity failed! Restore it to default value in configuration file!")
                model["DG"]["PMAX"] = configuration_default_generators.default_AC_generator_parameters["PMAX"]
        if type(model["DG"]["PMIN"]) is not float and type(model["DG"]["PMIN"]) is not int:
            logger.error("The data format of diesel generator capacity is incorrect!")
            try:
                logger.warning("Try to fix the capacity of diesel generator")
                model["DG"]["PMIN"] = model["DG"]["PMIN"][0]
            except:
                logger.info(
                    "The correction of diesel generator capacity failed! Restore it to default value in configuration file!")
                model["DG"]["PMIN"] = configuration_default_generators.default_AC_generator_parameters["PMIN"]
        if model["DG"]["PMIN"] > model["DG"]["PMAX"]:
            logger.error("The maximal capacity of UG is smaller than the minimal capacity!")
            model["DG"]["PMIN"] = model["DG"]["PMAX"]
        if model["DG"]["QMIN"] > model["DG"]["QMAX"]:
            logger.error("The maximal reactive power capacity of UG is smaller than the minimal capacity!")
            model["DG"]["QMIN"] = model["DG"]["QMAX"]

        # 3) The input check of photovoltaic generators
        if len(model["PV"]["NPV"]) != T:
            logger.error("The size of photovoltaic generator status is incorrect!")
            logger.info("The status of photovoltaic generator has been reset to online!")
            model["PV"]["NPV"] = [configuration_default_generators.default_RES_generator_parameters["PMAX"]] * T
        if type(model["PV"]["PMAX"]) is not list:
            logger.error("The data format of photovoltaic generator capacity is incorrect!")
            try:
                logger.warning("Try to fix the capacity of photovoltaic generator")
                model["PV"]["PMAX"] = [model["PV"]["PMAX"][0]]*T
            except:
                logger.info(
                    "The correction of photovoltaic generator capacity failed! Restore it to default value in configuration file!")
                model["PV"]["PMAX"] = [configuration_default_generators.default_RES_generator_parameters["PMAX"]]*T


        # 4) The input check of wind turbine generators
        if len(model["WP"]["NWP"]) != T:
            logger.error("The size of WP status is incorrect!")
            logger.info("The status of WP has been reset to online!")
            model["WP"]["NPV"] = [configuration_default_generators.default_RES_generator_parameters["PMAX"]] * T
        if type(model["WP"]["PMAX"]) is not list:
            logger.error("The data format of WP capacity is incorrect!")
            try:
                logger.warning("Try to fix the capacity of WP")
                model["WP"]["PMAX"] = [model["WP"]["PMAX"][0]]*T
            except:
                logger.info("The correction of WP capacity failed! Restore it to default value in configuration file!")
                model["WP"]["PMAX"] = [configuration_default_generators.default_RES_generator_parameters["PMAX"]]*T

        # 5) The input check of critical AC load
        if len(model["Load_ac"]["STATUS"]) != T:
            logger.error("The size of critical AC load status is incorrect!")
            logger.info("The status of critical AC load has been reset to default value!")
            model["Load_ac"]["STATUS"] = [configuration_default_load.default_Load_AC["STATUS"]] * T
        if len(model["Load_ac"]["PD"]) != T:
            logger.error("The size of critical AC load profile is incorrect!")
            logger.info("The profile of critical AC load has been reset to default value!")
            model["Load_ac"]["PD"] = [configuration_default_load.default_Load_AC["PD"]] * T
        for i in range(T):
            if model["Load_ac"]["PD"][i] > model["Load_ac"]["STATUS"][i] * model["Load_ac"]["PDMAX"]:
                logger.error("The critical AC load is over current!")
                logger.info("The critical AC load is set to its default value!")
                model["Load_ac"]["PD"][i] = model["Load_ac"]["STATUS"][i] * model["Load_ac"]["PDMAX"]

        # 6) The input check of non-critical AC load
        if len(model["Load_uac"]["STATUS"]) != T:
            logger.error("The size of non-critical AC load status is incorrect!")
            logger.info("The status of non-critical AC load has been reset to default value!")
            model["Load_uac"]["STATUS"] = [configuration_default_load.default_Load_AC["STATUS"]] * T
        if len(model["Load_uac"]["PD"]) != T:
            logger.error("The size of non-critical AC load profile is incorrect!")
            logger.info("The profile of non-critical AC load has been reset to online!")
            model["Load_uac"]["PD"] = [configuration_default_load.default_Load_AC["PD"]] * T
        for i in range(T):
            if model["Load_uac"]["PD"][i] > model["Load_uac"]["STATUS"][i] * model["Load_uac"]["PDMAX"]:
                logger.error("The non-critical AC load is over current!")
                logger.info("The non-critical AC load is set to its default value!")
                model["Load_uac"]["PD"][i] = model["Load_uac"]["STATUS"][i] * model["Load_uac"]["PDMAX"]

        # 7) The input check of critical AC load
        if len(model["Load_dc"]["STATUS"]) != T:
            logger.error("The size of critical DC load status is incorrect!")
            logger.info("The status of critical DC load has been reset to default value!")
            model["Load_dc"]["STATUS"] = [configuration_default_load.default_Load_DC["STATUS"]] * T
        if len(model["Load_dc"]["PD"]) != T:
            logger.error("The size of critical DC load profile is incorrect!")
            logger.info("The profile of critical DC load has been reset to default value!")
            model["Load_dc"]["PD"] = [configuration_default_load.default_Load_DC["PD"]] * T
        for i in range(T):
            if model["Load_dc"]["PD"][i] > model["Load_dc"]["STATUS"][i] * model["Load_dc"]["PDMAX"]:
                logger.error("The critical DC load is over current!")
                logger.info("The critical DC load is set to its default value!")
                model["Load_dc"]["PD"][i] = model["Load_dc"]["STATUS"][i] * model["Load_dc"]["PDMAX"]

        # 8) The input check of non-critical AC load
        if len(model["Load_udc"]["STATUS"]) != T:
            logger.error("The size of non-critical DC load status is incorrect!")
            logger.info("The status of non-critical DC load has been reset to default value!")
            model["Load_udc"]["STATUS"] = [configuration_default_load.default_Load_DC["STATUS"]] * T
        if len(model["Load_udc"]["PD"]) != T:
            logger.error("The size of non-critical DC load profile is incorrect!")
            logger.info("The profile of non-critical DC load has been reset to online!")
            model["Load_udc"]["PD"] = [configuration_default_load.default_Load_DC["PD"]] * T
        for i in range(T):
            if model["Load_udc"]["PD"][i] > model["Load_udc"]["STATUS"][i] * model["Load_udc"]["PDMAX"]:
                logger.error("The non-critical DC load is over current!")
                logger.info("The non-critical DC load is set to its default value!")
                model["Load_udc"]["PD"][i] = model["Load_udc"]["STATUS"][i] * model["Load_udc"]["PDMAX"]

        # 9) The input check for BIC convertors
        if len(model["BIC"]["STATUS"]) != T:
            logger.error("The size of BIC status is incorrect!")
            logger.info("The status of BIC has been reset to default value!")
            model["BIC"]["STATUS"] = [configuration_convertors.BIC["STATUS"]] * T

        # 10) The input check for ESSs
        if len(model["ESS"]["STATUS"]) != T:
            logger.error("The size of ESS status is incorrect!")
            logger.info("The status of ESS has been reset to default value!")
            model["ESS"]["STATUS"] = [configuration_convertors.BIC["STATUS"]] * T

        # 11) The input check for Transmission lines
        if len(model["LINE"]["STATUS"]) != T:
            logger.error("The size of  transmission line status is incorrect!")
            logger.info("The status of transmission line has been reset to default value!")
            model["LINE"]["STATUS"] = [configuration_convertors.BIC["LINE"]] * T

        return model