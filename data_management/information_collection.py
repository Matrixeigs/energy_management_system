import threading
from data_management.information_management import information_receive_send


class Information_Collection_Thread(threading.Thread):
    # Thread operation with time control and return value
    def __init__(self, socket, info, local_models, t):
        threading.Thread.__init__(self)
        self.socket = socket
        self.info = info
        self.local_models = local_models
        self.t = t

    def run(self):
        self.local_models = information_collection_updating(self.socket, self.info, self.local_models, self.t)


def information_collection_updating(*args):
    socket = args[0]
    info = args[1]
    models = args[2]
    T = args[3]

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

    models["DG"]["GEN_STATUS"] = [0]*T
    models["UG"]["GEN_STATUS"] = [0]*T  # The microgrid is isolated.

    models["Load_ac"]["PD"] = [0]*T
    models["Load_dc"]["PD"] = [0]*T
    models["Load_uac"]["PD"] = [0]*T
    models["Load_udc"]["PD"] = [0]*T

    models["PV"]["PG"] = [0]*T
    models["WP"]["PG"] = [0]*T

    for i in range(T):
        if type(dg_info.GEN_STATUS) is list:
            models["DG"]["GEN_STATUS"][i] = dg_info.GEN_STATUS[i]
        else:
            models["DG"]["GEN_STATUS"][i] = dg_info.GEN_STATUS
        if type(ug_info.GEN_STATUS) is list:
            models["UG"]["GEN_STATUS"][i] = ug_info.GEN_STATUS[i]  # The microgrid is isolated.
        else:
            models["UG"]["GEN_STATUS"][i] = ug_info.GEN_STATUS

        if type(load_ac_info.PD) is list:
            models["Load_ac"]["PD"][i] = load_ac_info.PD[i]
            models["Load_dc"]["PD"][i] = load_dc_info.PD[i]
            models["Load_uac"]["PD"][i] = load_uac_info.PD[i]
            models["Load_udc"]["PD"][i] = load_udc_info.PD[i]

            models["PV"]["PG"][i] = pv_info.PG[i]
            models["WP"]["PG"][i] = wp_info.PG[i]
        else:
            models["Load_ac"]["PD"][i] = load_ac_info.PD
            models["Load_dc"]["PD"][i] = load_dc_info.PD
            models["Load_uac"]["PD"][i] = load_uac_info.PD
            models["Load_udc"]["PD"][i] = load_udc_info.PD

            models["PV"]["PG"][i] = pv_info.PG
            models["WP"]["PG"][i] = wp_info.PG

    if type(ess_info.SOC) is list:
        models["ESS"]["SOC"] = float(ess_info.SOC[0])  # The initial energy state in the storage systems.
    else:
        models["ESS"]["SOC"] = float(ess_info.SOC)

    return models
