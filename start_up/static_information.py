"""
Static information generation for energy management system

"""

import modelling.local_ems_pb2 as static_model
import time

def static_information_generation(*args):
    # Static informaiton generation for local ems
    local_models = args[0]

    info = static_model.local_sources_model()
    dg_info = static_model.local_sources_model.DgType()  # The utility grid is modelled as a generation as well.
    ug_info = static_model.local_sources_model.DgType()  # The utility grid is modelled as a generation as well.
    ess_info = static_model.local_sources_model.EssType()
    pv_info = static_model.local_sources_model.PvType()
    wp_info = static_model.local_sources_model.WpType()
    load_ac_info = static_model.local_sources_model.Load_AC_Type()
    load_uac_info = static_model.local_sources_model.Load_AC_Type()
    load_dc_info = static_model.local_sources_model.Load_DC_Type()
    load_udc_info = static_model.local_sources_model.Load_DC_Type()
    bic_info = static_model.local_sources_model.Convertor_Type()
    # Update the static information
    info.area = 2  # The area information
    info.time_stamp = round(time.time())  # The information generation time

    # The utility grid part
    ug_info.dg_id = 0
    ug_info.GEN_STATUS = local_models["UG"]["GEN_STATUS"]  # The utility grid is not available.
    ug_info.PMIN = local_models["UG"]["PMIN"]
    ug_info.PMAX = local_models["UG"]["PMAX"]
    ug_info.QMIN = local_models["UG"]["QMIN"]
    ug_info.QMAX = local_models["UG"]["QMAX"]
    ug_info.SMAX = local_models["UG"]["SMAX"]
    ug_info.RAMP_AGC = local_models["UG"]["RAMP_AGC"]
    ug_info.RAMP_10 = local_models["UG"]["RAMP_10"]
    ug_info.COST_START_UP = local_models["UG"]["COST_START_UP"]
    ug_info.COST_SHUT_DOWN = local_models["UG"]["COST_SHUT_DOWN"]
    ug_info.COST_MODEL = local_models["UG"]["COST_MODEL"]  # Linear model
    ug_info.NCOST = local_models["UG"]["NCOST"]  # There is only one parameter.
    ug_info.COST.extend(local_models["UG"]["COST"])

    # The diesel generation part
    dg_info.dg_id = 1
    dg_info.GEN_STATUS = local_models["DG"]["GEN_STATUS"]  # The diesel generator is available.
    dg_info.PMIN = local_models["DG"]["PMIN"]
    dg_info.PMAX = local_models["DG"]["PMAX"]
    dg_info.QMIN = local_models["DG"]["QMIN"]
    dg_info.QMAX = local_models["DG"]["QMAX"]
    dg_info.SMAX = local_models["DG"]["SMAX"]
    dg_info.RAMP_AGC = local_models["DG"]["RAMP_AGC"]
    dg_info.RAMP_10 = local_models["DG"]["RAMP_10"]
    dg_info.COST_START_UP = local_models["DG"]["COST_START_UP"]
    dg_info.COST_SHUT_DOWN = local_models["DG"]["COST_SHUT_DOWN"]
    dg_info.COST_MODEL = local_models["DG"]["COST_MODEL"]
    dg_info.NCOST = local_models["DG"]["NCOST"]
    dg_info.COST.extend(local_models["DG"]["COST"])
    # Add result back to the information set.
    info.dg.extend([ug_info, dg_info])

    # The energy storage system part
    ess_info.ess_id = 1
    ess_info.ESS_STATUS = 1  # The energy storage system is online
    ess_info.CAP = local_models["ESS"]["CAP"]
    ess_info.PMAX_DIS = local_models["ESS"]["PMAX_DIS"]
    ess_info.PMAX_CH = local_models["ESS"]["PMAX_CH"]
    ess_info.EFF_DIS = local_models["ESS"]["EFF_DIS"]
    ess_info.EFF_CH = local_models["ESS"]["EFF_CH"]
    ess_info.SOC_MAX = local_models["ESS"]["SOC_MAX"]
    ess_info.SOC_MIN = local_models["ESS"]["SOC_MIN"]
    ess_info.COST_MODEL = local_models["ESS"]["COST_MODEL"]
    ess_info.NCOST_DIS = local_models["ESS"]["NCOST_DIS"]
    ess_info.COST_DIS.extend(local_models["ESS"]["COST_DIS"])
    ess_info.NCOST_CH = local_models["ESS"]["NCOST_CH"]
    ess_info.COST_CH.extend(local_models["ESS"]["COST_CH"])

    info.ess.extend([ess_info])
    # The pv group
    pv_info.NPV = local_models["PV"]["PMAX"]
    pv_info.TYPE = 1
    pv_info.GEN_STATUS = local_models["PV"]["GEN_STATUS"]
    pv_info.PMAX = local_models["PV"]["PMAX"]
    pv_info.PMIN = local_models["PV"]["PMIN"]
    pv_info.QMAX = local_models["PV"]["QMAX"]
    pv_info.QMIN = local_models["PV"]["QMIN"]
    pv_info.SMAX = local_models["PV"]["SMAX"]
    pv_info.COST = local_models["PV"]["COST"]

    info.pv.extend([pv_info])
    # The wp group
    wp_info.NWP = local_models["WP"]["PMAX"]
    wp_info.TYPE = 2
    wp_info.GEN_STATUS = local_models["WP"]["GEN_STATUS"]
    wp_info.PMAX = local_models["WP"]["PMAX"]
    wp_info.PMIN = local_models["WP"]["PMIN"]
    wp_info.QMAX = local_models["WP"]["QMAX"]
    wp_info.QMIN = local_models["WP"]["QMIN"]
    wp_info.SMAX = local_models["WP"]["SMAX"]
    wp_info.COST = local_models["WP"]["COST"]

    info.wp.extend([wp_info])

    # The load part
    # AC critical load
    load_ac_info.STATUS = local_models["Load_ac"]["STATUS"]
    load_ac_info.PDMAX = local_models["Load_ac"]["PDMAX"]
    load_ac_info.PDMIN = local_models["Load_ac"]["PDMIN"]
    load_ac_info.FLEX = local_models["Load_ac"]["FLEX"]  # 0=critical load;1=non_critical load
    load_ac_info.MODEL = local_models["Load_ac"]["MODEL"]
    load_ac_info.COST_MODEL = local_models["Load_ac"]["COST_MODEL"]
    load_ac_info.NCOST = local_models["Load_ac"]["NCOST"]
    load_ac_info.COST.extend(local_models["Load_ac"]["COST"])

    # AC non-critical load
    load_uac_info.STATUS = local_models["Load_uac"]["STATUS"]
    load_uac_info.PDMAX = local_models["Load_uac"]["PDMAX"]
    load_uac_info.PDMIN = local_models["Load_uac"]["PDMIN"]
    load_uac_info.FLEX = local_models["Load_uac"]["FLEX"]  # 0=critical load;1=non_critical load
    load_uac_info.MODEL = local_models["Load_uac"]["MODEL"]
    load_uac_info.COST_MODEL = local_models["Load_uac"]["COST_MODEL"]
    load_uac_info.NCOST = local_models["Load_uac"]["NCOST"]
    load_uac_info.COST.extend(local_models["Load_uac"]["COST"])

    info.load_ac.extend([load_ac_info, load_uac_info])

    # DC critial load
    load_dc_info.STATUS = local_models["Load_dc"]["STATUS"]
    load_dc_info.PDMAX = local_models["Load_dc"]["PDMAX"]
    load_dc_info.PDMIN = local_models["Load_dc"]["PDMIN"]
    load_dc_info.FLEX = local_models["Load_dc"]["FLEX"]  # 0=critical load;1=non_critical load
    load_dc_info.MODEL = local_models["Load_dc"]["MODEL"]
    load_dc_info.COST_MODEL = local_models["Load_dc"]["COST_MODEL"]
    load_dc_info.NCOST = local_models["Load_dc"]["NCOST"]
    load_dc_info.COST.extend(local_models["Load_dc"]["COST"])
    # DC non-critical load
    load_udc_info.STATUS = local_models["Load_udc"]["STATUS"]
    load_udc_info.PDMAX = local_models["Load_udc"]["PDMAX"]
    load_udc_info.PDMIN = local_models["Load_udc"]["PDMIN"]
    load_udc_info.FLEX = local_models["Load_udc"]["FLEX"]  # 0=critical load;1=non_critical load
    load_udc_info.MODEL = local_models["Load_udc"]["MODEL"]
    load_udc_info.COST_MODEL = local_models["Load_udc"]["COST_MODEL"]
    load_udc_info.NCOST = local_models["Load_udc"]["NCOST"]
    load_udc_info.COST.extend(local_models["Load_udc"]["COST"])

    info.load_dc.extend([load_dc_info, load_udc_info])

    # BIC information
    bic_info.STATUS = 1
    bic_info.CAP = local_models["BIC"]["CAP"]
    bic_info.EFF_AC2DC = local_models["BIC"]["EFF_AC2DC"]
    bic_info.EFF_DC2AC = local_models["BIC"]["EFF_DC2AC"]
    info.bic.extend([bic_info])

    return info  # The information structure.
