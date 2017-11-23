# Start up operation procedure for universal ems
# short, middle and long term operating models are generated for the short, middle and long term operation respectively.
from modelling import generators, loads, energy_storage_systems, convertors, transmission_lines  # Import modellings
from utils import Logger
from configuration.configuration_time_line import default_look_ahead_time_step# The look ahead time is adopted to
from copy import deepcopy

class start_up_lems():
    ## The start up class of UEMS
    def start_up(*args):
        logger = Logger("local_ems_start_up")
        # Obtain static information of the local ems
        # Update the local EMS parameters
        local_models = {"DG": generators.Generator_AC.copy(),
                        "UG": generators.Generator_AC.copy(),
                        "Load_ac": loads.Load_AC.copy(),
                        "Load_uac": loads.Load_AC.copy(),
                        "BIC": convertors.BIC.copy(),
                        "ESS": energy_storage_systems.BESS.copy(),
                        "PV": generators.Generator_RES.copy(),
                        "WP": generators.Generator_RES.copy(),
                        "Load_dc": loads.Load_DC.copy(),
                        "Load_udc": loads.Load_DC.copy(),
                        "PMG": 0,
                        "V_DC": 0}
        local_models["PV"]["NPV"] = local_models["PV"]["PMAX"]
        local_models["WP"]["NWP"] = local_models["WP"]["PMAX"]

        T_short = default_look_ahead_time_step["Look_ahead_time_opf_time_step"] # The look ahead time step for short term operation
        T_middle = default_look_ahead_time_step["Look_ahead_time_ed_time_step"]# The look ahead time step for middle term operation
        T_long = default_look_ahead_time_step["Look_ahead_time_uc_time_step"]# The look ahead time step for long term operation
        # Update information
        local_model_short = deepcopy(local_models)
        local_model_middle = deepcopy(local_models)
        local_model_long = deepcopy(local_models)

        # Generate middle term operation model for local ems, these information should be updated according to the database of resource manager
        local_model_middle["UG"]["GEN_STATUS"] = [local_model_middle["UG"]["GEN_STATUS"]] * T_middle
        local_model_middle["DG"]["GEN_STATUS"] = [local_model_middle["DG"]["GEN_STATUS"]] * T_middle
        local_model_middle["PV"]["NPV"] = [local_model_middle["PV"]["NPV"]] * T_middle
        local_model_middle["PV"]["PMAX"] = [local_model_middle["PV"]["PMAX"]] * T_middle
        local_model_middle["WP"]["NWP"] = [local_model_middle["WP"]["NWP"]] * T_middle
        local_model_middle["WP"]["PMAX"] = [local_model_middle["WP"]["PMAX"]] * T_middle
        local_model_middle["Load_ac"]["STATUS"] = [local_model_middle["Load_ac"]["STATUS"]] * T_middle
        local_model_middle["Load_uac"]["STATUS"] = [local_model_middle["Load_uac"]["STATUS"]] * T_middle
        local_model_middle["Load_dc"]["STATUS"] = [local_model_middle["Load_dc"]["STATUS"]] * T_middle
        local_model_middle["Load_udc"]["STATUS"] = [local_model_middle["Load_udc"]["STATUS"]] * T_middle
        # Generate long term operation model for local ems
        local_model_long["UG"]["GEN_STATUS"] = [local_model_long["UG"]["GEN_STATUS"]] * T_long
        local_model_long["DG"]["GEN_STATUS"] = [local_model_long["DG"]["GEN_STATUS"]] * T_long
        local_model_long["PV"]["NPV"] = [local_model_long["PV"]["NPV"]] * T_long
        local_model_long["PV"]["PMAX"] = [local_model_long["PV"]["PMAX"]] * T_long
        local_model_long["WP"]["NWP"] = [local_model_long["WP"]["NWP"]] * T_long
        local_model_long["WP"]["PMAX"] = [local_model_long["WP"]["PMAX"]] * T_long
        local_model_long["Load_ac"]["STATUS"] = [local_model_long["Load_ac"]["STATUS"]] * T_long
        local_model_long["Load_uac"]["STATUS"] = [local_model_long["Load_uac"]["STATUS"]] * T_long
        local_model_long["Load_dc"]["STATUS"] = [local_model_long["Load_dc"]["STATUS"]] * T_long
        local_model_long["Load_udc"]["STATUS"] = [local_model_long["Load_udc"]["STATUS"]] * T_long


        return local_model_short, local_model_middle, local_model_long
