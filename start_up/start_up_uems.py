# Start up operation procedure for universal ems
# short, middle and long term operating models are generated for the short, middle and long term operation respectively.
import time
from modelling import local_ems_pb2
from data_management.information_management import information_receive_send
from modelling import generators, loads, energy_storage_systems, convertors, transmission_lines  # Import modellings
from start_up import static_information_update
from utils import Logger
from configuration.configuration_time_line import default_look_ahead_time_step# The look ahead time is adopted to
from copy import deepcopy
class start_up_ems():
    ## The start up class of UEMS
    def start_up(*args):
        socket = args[0]

        t0 = time.time()
        Conenction_time_max = 100
        logger = Logger("Universal_ems_start_up")
        Operation_mode = 1  # 1=Work as a universal EMS; 2=Work as a local EMS.

        while True:
            message = socket.recv()
            if message == b"ConnectionRequest":
                logger.info("The connection between the local EMS and universal EMS establishes!")
                socket.send(b"Start!")
                break
            else:
                logger.error("Waiting for the connection between the local EMS and universal EMS!")
                time.sleep(1)  # Waiting for next time connection

            if time.time() > t0 + Conenction_time_max:  # Timeout error detection
                logger.error("Connection is timeout!")
                logger.warning("Uems works as a local ems now!")
                Operation_mode = 2  # Change the working mode of universal energy management system
                break
        if Operation_mode == 1: # The connection can be established!
            # Obtain static information of the local ems
            static_info = local_ems_pb2.local_sources_model()
            static_info = information_receive_send.information_receive(socket, static_info, 2)
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

            universal_models = {"DG": generators.Generator_AC.copy(),
                                "UG": generators.Generator_AC.copy(),
                                "Load_ac": loads.Load_AC.copy(),
                                "Load_uac": loads.Load_AC.copy(),
                                "BIC": convertors.BIC.copy(),
                                "ESS": energy_storage_systems.BESS.copy(),
                                "PV": generators.Generator_RES.copy(),
                                "WP": generators.Generator_RES.copy(),
                                "Load_dc": loads.Load_DC.copy(),
                                "Load_udc": loads.Load_DC.copy(),
                                "LINE": transmission_lines.Line.copy(),
                                "PMG": 0,
                                "V_DC": 0}
            universal_models["PV"]["NPV"] = universal_models["PV"]["PMAX"]
            universal_models["WP"]["NWP"] = universal_models["WP"]["PMAX"]
            # Update the techinical and economic parameters of local sources
            local_models = static_information_update.information_update(local_models, static_info)

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

            universal_model_short = deepcopy(universal_models)
            universal_model_middle = deepcopy(universal_models)
            universal_model_long = deepcopy(universal_models)

            # Generate middle term operation model for universal ems, these information should be updated according to the database of resource manager
            universal_model_middle["UG"]["GEN_STATUS"] = [universal_model_middle["UG"]["GEN_STATUS"]] * T_middle
            universal_model_middle["DG"]["GEN_STATUS"] = [universal_model_middle["DG"]["GEN_STATUS"]] * T_middle
            universal_model_middle["PV"]["NPV"] = [universal_model_middle["PV"]["NPV"]] * T_middle
            universal_model_middle["PV"]["PMAX"] = [universal_model_middle["PV"]["PMAX"]] * T_middle
            universal_model_middle["WP"]["NWP"] = [universal_model_middle["WP"]["NWP"]] * T_middle
            universal_model_middle["WP"]["PMAX"] = [universal_model_middle["WP"]["PMAX"]] * T_middle
            universal_model_middle["Load_ac"]["STATUS"] = [universal_model_middle["Load_ac"]["STATUS"]] * T_middle
            universal_model_middle["Load_uac"]["STATUS"] = [universal_model_middle["Load_uac"]["STATUS"]] * T_middle
            universal_model_middle["Load_dc"]["STATUS"] = [universal_model_middle["Load_dc"]["STATUS"]] * T_middle
            universal_model_middle["Load_udc"]["STATUS"] = [universal_model_middle["Load_udc"]["STATUS"]] * T_middle
            universal_model_middle["LINE"]["STATUS"] = [universal_model_middle["LINE"]["STATUS"]] * T_middle

            # Generate long term operation model for universal ems
            universal_model_long["UG"]["GEN_STATUS"] = [universal_model_long["UG"]["GEN_STATUS"]] * T_long
            universal_model_long["DG"]["GEN_STATUS"] = [universal_model_long["DG"]["GEN_STATUS"]] * T_long
            universal_model_long["PV"]["NPV"] = [universal_model_long["PV"]["NPV"]] * T_long
            universal_model_long["PV"]["PMAX"] = [universal_model_long["PV"]["PMAX"]] * T_long
            universal_model_long["WP"]["NWP"] = [universal_model_long["WP"]["NWP"]] * T_long
            universal_model_long["WP"]["PMAX"] = [universal_model_long["WP"]["PMAX"]] * T_long
            universal_model_long["Load_ac"]["STATUS"] = [universal_model_long["Load_ac"]["STATUS"]] * T_long
            universal_model_long["Load_uac"]["STATUS"] = [universal_model_long["Load_uac"]["STATUS"]] * T_long
            universal_model_long["Load_dc"]["STATUS"] = [universal_model_long["Load_dc"]["STATUS"]] * T_long
            universal_model_long["Load_udc"]["STATUS"] = [universal_model_long["Load_udc"]["STATUS"]] * T_long
            universal_model_long["LINE"]["STATUS"] = [universal_model_long["LINE"]["STATUS"]] * T_long

            return local_model_short, local_model_middle, local_model_long, universal_model_short,universal_model_middle,universal_model_long, Operation_mode

        else:
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

            T_short = default_look_ahead_time_step[
                "Look_ahead_time_opf_time_step"]  # The look ahead time step for short term operation
            T_middle = default_look_ahead_time_step[
                "Look_ahead_time_ed_time_step"]  # The look ahead time step for middle term operation
            T_long = default_look_ahead_time_step[
                "Look_ahead_time_uc_time_step"]  # The look ahead time step for long term operation
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
            return local_model_short, local_model_middle, local_model_long, Operation_mode

