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
    command_type = info.COMMAND_TYPE

    ### Update the availability information

    models["DG"]["GEN_STATUS"] = [0]*T
    models["UG"]["GEN_STATUS"] = [0]*T  # The microgrid is isolated.

    models["Load_ac"]["PD"] = [0]*T
    models["Load_dc"]["PD"] = [0]*T
    models["Load_uac"]["PD"] = [0]*T
    models["Load_udc"]["PD"] = [0]*T

    models["PV"]["PG"] = [0]*T
    models["WP"]["PG"] = [0]*T
    models["COMMAND_TYPE"] = command_type

    if T==1: # The single time step operation
        models["DG"]["GEN_STATUS"] = dg_info.GEN_STATUS
        models["UG"]["GEN_STATUS"] = ug_info.GEN_STATUS  # The microgrid is isolated.

        models["Load_ac"]["PD"] = load_ac_info.PD
        models["Load_dc"]["PD"] = load_dc_info.PD
        models["Load_uac"]["PD"] = load_uac_info.PD
        models["Load_udc"]["PD"] = load_udc_info.PD

        models["PV"]["PG"] = pv_info.PG
        models["WP"]["PG"] = wp_info.PG

    else:
        for i in range(T):
            models["DG"]["GEN_STATUS"][i] = dg_info.GEN_STATUS._values[i]
            models["UG"]["GEN_STATUS"][i] = ug_info.GEN_STATUS._values[i]  # The microgrid is isolated.

            models["Load_ac"]["PD"][i] = load_ac_info.PD._values[i]
            models["Load_dc"]["PD"][i] = load_dc_info.PD._values[i]
            models["Load_uac"]["PD"][i] = load_uac_info.PD._values[i]
            models["Load_udc"]["PD"][i] = load_udc_info.PD._values[i]

            models["PV"]["PG"][i] = pv_info.PG._values[i]
            models["WP"]["PG"][i] = wp_info.PG._values[i]

        models["ESS"]["SOC"] = float(ess_info.SOC._values[0])  # The initial energy state in the storage systems.

    if command_type == 1: # The set-point tracing method
        if T == 1:
            models["UG"]["COMMAND_PG"] = ug_info.PG
            models["UG"]["COMMAND_QG"] = ug_info.QG
            models["UG"]["COMMAND_RG"] = ug_info.RG

            models["DG"]["COMMAND_PG"] = dg_info.PG
            models["DG"]["COMMAND_QG"] = ug_info.QG
            models["DG"]["COMMAND_RG"] = ug_info.RG

            models["ESS"]["SOC"] = ess_info.SOC
            models["ESS"]["COMMAND_PG"] = ess_info.PG
            models["ESS"]["COMMAND_RG"] = ess_info.RG

            models["PMG"] = info.PMG

            models["BIC"]["COMMAND_AC2DC"] = bic_info.PAC2DC
            models["BIC"]["COMMAND_DC2AC"] = bic_info.PDC2AC

            models["PV"]["COMMAND_CURT"] = pv_info.COMMAND_CURT
            models["WP"]["COMMAND_CURT"] = wp_info.COMMAND_CURT

            models["Load_ac"]["COMMAND_SHED"] = load_ac_info.COMMAND_SHED
            models["Load_uac"]["COMMAND_SHED"] = load_uac_info.COMMAND_SHED
            models["Load_dc"]["COMMAND_SHED"] = load_dc_info.COMMAND_SHED
            models["Load_udc"]["COMMAND_SHED"] = load_udc_info.COMMAND_SHED



    return models
