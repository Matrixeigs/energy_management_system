# Update the techinical and economic parameters of local sources
def information_update(*args):
    local_models = args[0]
    info = args[1]
    local_models["UG"]["AREA"] = info.area
    local_models["UG"]["GEN_STATUS"] = info.dg[0].GEN_STATUS
    local_models["UG"]["PMIN"] = info.dg[0].PMIN
    local_models["UG"]["PMAX"] = info.dg[0].PMAX
    local_models["UG"]["QMIN"] = info.dg[0].QMIN
    local_models["UG"]["QMAX"] = info.dg[0].QMAX
    local_models["UG"]["SMAX"] = info.dg[0].SMAX
    local_models["UG"]["RAMP_AGC"] = info.dg[0].RAMP_AGC
    local_models["UG"]["RAMP_10"] = info.dg[0].RAMP_10
    local_models["UG"]["COST_START_UP"] = info.dg[0].COST_START_UP
    local_models["UG"]["COST_SHUT_DOWN"] = info.dg[0].COST_SHUT_DOWN
    local_models["UG"]["COST_MODEL"] = info.dg[0].COST_MODEL
    local_models["UG"]["NCOST"] = info.dg[0].NCOST
    local_models["UG"]["COST"] = info.dg[0].COST

    local_models["DG"]["AREA"] = info.area
    local_models["DG"]["GEN_STATUS"] = info.dg[1].GEN_STATUS
    local_models["DG"]["PMIN"] = info.dg[1].PMIN
    local_models["DG"]["PMAX"] = info.dg[1].PMAX
    local_models["DG"]["QMIN"] = info.dg[1].QMIN
    local_models["DG"]["QMAX"] = info.dg[1].QMAX
    local_models["DG"]["SMAX"] = info.dg[1].SMAX
    local_models["DG"]["RAMP_AGC"] = info.dg[1].RAMP_AGC
    local_models["DG"]["RAMP_10"] = info.dg[1].RAMP_10
    local_models["DG"]["COST_START_UP"] = info.dg[1].COST_START_UP
    local_models["DG"]["COST_SHUT_DOWN"] = info.dg[1].COST_SHUT_DOWN
    local_models["DG"]["COST_MODEL"] = info.dg[1].COST_MODEL
    local_models["DG"]["NCOST"] = info.dg[1].NCOST
    local_models["DG"]["COST"] = info.dg[1].COST

    local_models["ESS"]["AREA"] = info.area
    local_models["ESS"]["CAP"] = info.ess[0].CAP
    local_models["ESS"]["PMAX_DIS"] = info.ess[0].PMAX_DIS
    local_models["ESS"]["PMAX_CH"] = info.ess[0].PMAX_CH
    local_models["ESS"]["EFF_DIS"] = info.ess[0].EFF_DIS
    local_models["ESS"]["EFF_CH"] = info.ess[0].EFF_CH
    local_models["ESS"]["SOC_MAX"] = info.ess[0].SOC_MAX
    local_models["ESS"]["SOC_MIN"] = info.ess[0].SOC_MIN
    local_models["ESS"]["COST_MODEL"] = info.ess[0].COST_MODEL
    local_models["ESS"]["NCOST_DIS"] = info.ess[0].NCOST_DIS
    local_models["ESS"]["COST_DIS"] = info.ess[0].COST_DIS
    local_models["ESS"]["NCOST_CH"] = info.ess[0].NCOST_CH
    local_models["ESS"]["COST_CH"] = info.ess[0].COST_CH

    local_models["PV"]["AREA"] = info.area
    local_models["PV"]["GEN_STATUS"] = info.pv[0].GEN_STATUS
    local_models["PV"]["PMAX"] = info.pv[0].PMAX
    local_models["PV"]["PMIN"] = info.pv[0].PMIN
    local_models["PV"]["QMAX"] = info.pv[0].QMAX
    local_models["PV"]["QMIN"] = info.pv[0].QMIN
    local_models["PV"]["SMAX"] = info.pv[0].SMAX
    local_models["PV"]["COST"] = info.pv[0].COST

    local_models["WP"]["AREA"] = info.area
    local_models["WP"]["GEN_STATUS"] = info.wp[0].GEN_STATUS
    local_models["WP"]["PMAX"] = info.wp[0].PMAX
    local_models["WP"]["PMIN"] = info.wp[0].PMIN
    local_models["WP"]["QMAX"] = info.wp[0].QMAX
    local_models["WP"]["QMIN"] = info.wp[0].QMIN
    local_models["WP"]["SMAX"] = info.wp[0].SMAX
    local_models["WP"]["COST"] = info.wp[0].COST

    local_models["Load_ac"]["AREA"] = info.area
    local_models["Load_ac"]["STATUS"] = info.load_ac[0].STATUS
    local_models["Load_ac"]["PDMAX"] = info.load_ac[0].PDMAX
    local_models["Load_ac"]["PDMIN"] = info.load_ac[0].PDMIN
    local_models["Load_ac"]["FLEX"] = info.load_ac[0].FLEX
    local_models["Load_ac"]["MODEL"] = info.load_ac[0].MODEL
    local_models["Load_ac"]["COST_MODEL"] = info.load_ac[0].COST_MODEL
    local_models["Load_ac"]["NCOST"] = info.load_ac[0].NCOST
    local_models["Load_ac"]["COST"] = info.load_ac[0].COST

    local_models["Load_uac"]["AREA"] = info.area
    local_models["Load_uac"]["STATUS"] = info.load_ac[1].STATUS
    local_models["Load_uac"]["PDMAX"] = info.load_ac[1].PDMAX
    local_models["Load_uac"]["PDMIN"] = info.load_ac[1].PDMIN
    local_models["Load_uac"]["FLEX"] = info.load_ac[1].FLEX
    local_models["Load_uac"]["MODEL"] = info.load_ac[1].MODEL
    local_models["Load_uac"]["COST_MODEL"] = info.load_ac[1].COST_MODEL
    local_models["Load_uac"]["NCOST"] = info.load_ac[1].NCOST
    local_models["Load_uac"]["COST"] = info.load_ac[1].COST

    local_models["Load_dc"]["AREA"] = info.area
    local_models["Load_dc"]["STATUS"] = info.load_dc[0].STATUS
    local_models["Load_dc"]["PDMAX"] = info.load_dc[0].PDMAX
    local_models["Load_dc"]["PDMIN"] = info.load_dc[0].PDMIN
    local_models["Load_dc"]["FLEX"] = info.load_dc[0].FLEX
    local_models["Load_dc"]["MODEL"] = info.load_dc[0].MODEL
    local_models["Load_dc"]["COST_MODEL"] = info.load_dc[0].COST_MODEL
    local_models["Load_dc"]["NCOST"] = info.load_dc[0].NCOST
    local_models["Load_dc"]["COST"] = info.load_dc[0].COST

    local_models["Load_udc"]["AREA"] = info.area
    local_models["Load_udc"]["STATUS"] = info.load_dc[1].STATUS
    local_models["Load_udc"]["PDMAX"] = info.load_dc[1].PDMAX
    local_models["Load_udc"]["PDMIN"] = info.load_dc[1].PDMIN
    local_models["Load_udc"]["FLEX"] = info.load_dc[1].FLEX
    local_models["Load_udc"]["MODEL"] = info.load_dc[1].MODEL
    local_models["Load_udc"]["COST_MODEL"] = info.load_dc[1].COST_MODEL
    local_models["Load_udc"]["NCOST"] = info.load_dc[1].NCOST
    local_models["Load_udc"]["COST"] = info.load_dc[1].COST

    local_models["BIC"]["AREA"] = info.area
    local_models["BIC"]["CAP"] = info.bic[0].CAP
    local_models["BIC"]["EFF_AC2DC"] = info.bic[0].EFF_AC2DC
    local_models["BIC"]["EFF_DC2AC"] = info.bic[0].EFF_DC2AC

    return local_models