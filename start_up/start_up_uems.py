# Start up operation procedure for universal ems
import time
from modelling import local_ems_pb2
from data_management.information_management import information_receive_send
from modelling import generators, loads, energy_storage_systems, convertors, transmission_lines  # Import modellings
from start_up import static_information_update
from utils import Logger


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
        # Update the techinical and economic parameters of local sources
        local_models = static_information_update.information_update(local_models, static_info)

        return local_models, universal_models, Operation_mode
