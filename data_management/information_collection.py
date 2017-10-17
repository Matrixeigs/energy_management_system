import threading
from data_management.information_management import information_receive_send


class Information_Collection_Thread(threading.Thread):
    # Thread operation with time control and return value
    def __init__(self, socket, info, local_models):
        threading.Thread.__init__(self)
        self.socket = socket
        self.info = info
        self.local_models = local_models

    def run(self):
        self.local_models = information_collection_updating(self.socket, self.info, self.local_models)


def information_collection_updating(*args):
    socket = args[0]
    info = args[1]
    models = args[2]
    info = information_receive_send.information_receive(socket, info, 2)
    # Update profiles
    ug_info = info.dg[0]
    dg_info = info.dg[1]
    ess_info = info.ess[0]
    pv_info = info.pv[0]
    wp_info = info.wp[0]
    load_ac_info = info.load_ac[0]
    load_uac_info = info.load_ac[1]
    load_dc_info = info.load_dc[0]
    load_udc_info = info.load_dc[1]
    bic_info = info.bic[0]
    ### Update the availability information
    models["DG"]["GEN_STATUS"] = dg_info.GEN_STATUS
    models["UG"]["GEN_STATUS"] = ug_info.GEN_STATUS  # The microgrid is isolated.

    models["Load_ac"]["PD"] = load_ac_info.PD
    models["Load_dc"]["PD"] = load_dc_info.PD
    models["Load_uac"]["PD"] = load_uac_info.PD
    models["Load_udc"]["PD"] = load_udc_info.PD

    models["PV"]["PG"] = pv_info.PG
    models["WP"]["PG"] = wp_info.PG

    models["ESS"]["SOC"] = ess_info.SOC  # The initial energy state in the storage systems.

    return models
