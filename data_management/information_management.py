class information_receive_send():
    ## The message receive and send functions for the universal energy management system
    def information_receive(*args):  # Obtain information via socket
        socket = args[0]  # The socket information
        info = args[1]  # The information model
        info_type = args[2]  # The information type, 1= message, 2= Google protocal
        if info_type == 1:  # The informaiton model is a binary string.
            info = socket.recv()  # Receive information from given socket
        else:  # The informaiton model follows Google protocol.
            message = socket.recv()
            info.ParseFromString(message)

        # Return the information model
        return info

    def information_send(*args):  # Send information via socket
        socket = args[0]  # The socket information
        info = args[1]  # The information model
        info_type = args[2]  # The information type, 1= message, 2= Google protocal
        if info_type == 1:  # The informaiton model is a binary string..
            socket.send(info)
        else:  # The informaiton model follows Google protocol.
            message = info.SerializeToString()
            socket.send(message)


class information_formulation_extraction():
    ## Dynamic model formulation and extraction
    def info_formulation(*args):
        import modelling.information_exchange_pb2 as dynamic_model  # The information model

        model = args[0]
        Target_time = args[1]
        # 1) Initial dynamic model
        dynamic_info = dynamic_model.informaiton_exchange()
        #################################The information structure
        ug_info = dynamic_model.informaiton_exchange.DgType()
        dg_info = dynamic_model.informaiton_exchange.DgType()
        ess_info = dynamic_model.informaiton_exchange.EssType()
        pv_info = dynamic_model.informaiton_exchange.PvType()
        wp_info = dynamic_model.informaiton_exchange.WpType()
        load_ac_info = dynamic_model.informaiton_exchange.Load_AC_Type()
        load_dc_info = dynamic_model.informaiton_exchange.Load_DC_Type()
        load_uac_info = dynamic_model.informaiton_exchange.Load_AC_Type()
        load_udc_info = dynamic_model.informaiton_exchange.Load_DC_Type()
        bic_info = dynamic_model.informaiton_exchange.Convertor_Type()

        # Obtain information from the external systems
        dynamic_info.AREA = model["UG"]["AREA"]
        dynamic_info.TIME_STAMP = Target_time
        # Update utility grid information
        ug_info.DG_ID = 0
        ug_info.GEN_STATUS = model["UG"]["GEN_STATUS"]
        ug_info.PG = model["UG"]["COMMAND_SET_POINT_PG"]
        ug_info.QG = model["UG"]["COMMAND_SET_POINT_QG"]
        ug_info.RG = model["UG"]["COMMAND_RESERVE"]
        # Update dg part information
        dg_info.DG_ID = 1
        dg_info.GEN_STATUS = model["DG"]["GEN_STATUS"]
        dg_info.PG = model["DG"]["COMMAND_SET_POINT_PG"]
        dg_info.QG = model["DG"]["COMMAND_SET_POINT_QG"]
        dg_info.RG = model["DG"]["COMMAND_RESERVE"]

        dynamic_info.dg.extend([ug_info, dg_info])
        # Update ess part information
        ess_info.ESS_ID = 1
        ess_info.ESS_STATUS = 1
        ess_info.SOC = model["ESS"]["SOC"]
        ess_info.PG = model["ESS"]["COMMAND_PG"]
        ess_info.RG = model["ESS"]["COMMAND_RG"]
        dynamic_info.ess.extend([ess_info])

        # Update pv part information
        pv_info.NPV = model["PV"]["PMAX"]
        pv_info.PG = model["PV"]["PG"]
        pv_info.COMMAND_CURT = model["PV"]["COMMAND_CURT"]
        dynamic_info.pv.extend([pv_info])

        # Update wp part information
        wp_info.NWP = model["WP"]["PMAX"]
        wp_info.PG = model["WP"]["PG"]
        wp_info.COMMAND_CURT = model["WP"]["COMMAND_CURT"]
        dynamic_info.wp.extend([wp_info])
        # Update load_ac part information
        load_ac_info.PD = model["Load_ac"]["PD"]
        load_ac_info.QD = model["Load_ac"]["QD"]
        load_ac_info.COMMAND_SHED = model["Load_ac"]["COMMAND_SHED"]

        load_uac_info.PD = model["Load_uac"]["PD"]
        load_uac_info.QD = model["Load_uac"]["QD"]
        load_uac_info.COMMAND_SHED = model["Load_uac"]["COMMAND_SHED"]

        dynamic_info.load_ac.extend([load_ac_info, load_uac_info])
        # Update load_dc part information
        load_dc_info.PD = model["Load_dc"]["PD"]
        load_dc_info.COMMAND_SHED = model["Load_dc"]["COMMAND_SHED"]

        load_udc_info.PD = model["Load_udc"]["PD"]
        load_udc_info.COMMAND_SHED = model["Load_udc"]["COMMAND_SHED"]

        dynamic_info.load_dc.extend([load_dc_info, load_udc_info])
        # Update convertor part information
        bic_info.STATUS = 1
        bic_info.PAC2DC = model["BIC"]["COMMAND_AC2DC"]
        bic_info.PDC2AC = model["BIC"]["COMMAND_DC2AC"]

        dynamic_info.bic.extend([bic_info])

        dynamic_info.PMG = model["PMG"]
        dynamic_info.TIME_STAMP_COMMAND = Target_time

        return dynamic_info

    def info_extraction(*args):
        model = args[0]
        info = args[1]
        # The utility grid part
        model["UG"]["GEN_STATUS"] = info.dg[0].GEN_STATUS
        model["UG"]["COMMAND_SET_POINT_PG"] = info.dg[0].PG
        model["UG"]["COMMAND_SET_POINT_QG"] = info.dg[0].QG
        model["UG"]["COMMAND_RESERVE"] = info.dg[0].RG
        # Update dg part information
        model["DG"]["GEN_STATUS"] = info.dg[1].GEN_STATUS
        model["DG"]["COMMAND_SET_POINT_PG"] = info.dg[1].PG
        model["DG"]["COMMAND_SET_POINT_QG"] = info.dg[1].QG
        model["DG"]["COMMAND_RESERVE"] = info.dg[1].RG

        # Update ess part information
        model["ESS"]["COMMAND_PG"] = info.ess[0].PG

        # Update BIC part
        model["BIC"]["COMMAND_AC2DC"] = info.bic[0].PAC2DC
        model["BIC"]["COMMAND_DC2AC"] = info.bic[0].PDC2AC

        # Update pv part information
        model["PV"]["COMMAND_CURT"] = info.pv[0].COMMAND_CURT

        # Update wp part information
        model["WP"]["COMMAND_CURT"] = info.wp[0].COMMAND_CURT
        # Update load_ac part information
        model["Load_ac"]["COMMAND_SHED"] = info.load_ac[0].COMMAND_SHED
        model["Load_uac"]["COMMAND_SHED"] = info.load_ac[1].COMMAND_SHED

        model["Load_dc"]["COMMAND_SHED"] = info.load_dc[0].COMMAND_SHED
        model["Load_udc"]["COMMAND_SHED"] = info.load_dc[1].COMMAND_SHED

        model["PMG"] = info.PMG
        model["V_DC"] = info.V_DC

        return model


class information_formulation_extraction_dynamic():
    ## Dynamic model formulation for unit commitment and economic dispatch
    def info_formulation(*args):
        import modelling.dynamic_operation_pb2 as dynamic_model  # The information model
        from configuration.configuration_time_line import default_look_ahead_time_step
        from numpy import ones
        model = args[0]
        Target_time = args[1]
        Type = args[2]

        if Type == "UC":
            T = default_look_ahead_time_step["Look_ahead_time_uc_time_step"]
        else:
            T = default_look_ahead_time_step["Look_ahead_time_ed_time_step"]
        # 1) Initial dynamic model
        dynamic_info = dynamic_model.local_sources()
        #################################The information structure
        ug_info = dynamic_model.local_sources.DgType()
        dg_info = dynamic_model.local_sources.DgType()
        ess_info = dynamic_model.local_sources.EssType()
        pv_info = dynamic_model.local_sources.PvType()
        wp_info = dynamic_model.local_sources.WpType()
        load_ac_info = dynamic_model.local_sources.Load_AC_Type()
        load_dc_info = dynamic_model.local_sources.Load_DC_Type()
        load_uac_info = dynamic_model.local_sources.Load_AC_Type()
        load_udc_info = dynamic_model.local_sources.Load_DC_Type()
        bic_info = dynamic_model.local_sources.Convertor_Type()

        # Obtain information from the external systems
        dynamic_info.AREA = model["UG"]["AREA"]
        dynamic_info.TIME_STAMP = Target_time
        # Update utility grid information
        ug_info.ID = 0
        if type(model["UG"]["GEN_STATUS"]) is list:
            if len(model["UG"]["GEN_STATUS"]) != T:
                ug_info.GEN_STATUS.extend(model["UG"]["GEN_STATUS"] * T)
            else:
                ug_info.GEN_STATUS.extend(model["UG"]["GEN_STATUS"])
        elif type(model["UG"]["GEN_STATUS"]) is int:
            ug_info.GEN_STATUS.extend([model["UG"]["GEN_STATUS"]] * T)

        if type(model["UG"]["COMMAND_PG"]) is list:
            ug_info.PG.extend(model["UG"]["COMMAND_PG"])
        else:
            ug_info.PG.extend([model["UG"]["COMMAND_PG"]])

        if type(model["UG"]["COMMAND_RG"]) is list:
            ug_info.RG.extend(model["UG"]["COMMAND_RG"])
        else:
            ug_info.RG.extend([model["UG"]["COMMAND_RG"]])

        if type(model["UG"]["COMMAND_START_UP"]) is list:
            ug_info.COMMAND_STATUS.extend(model["UG"]["COMMAND_START_UP"])
        else:
            ug_info.COMMAND_STATUS.extend([model["UG"]["COMMAND_START_UP"]])

        # Update dg part information
        dg_info.ID = 1
        if type(model["DG"]["GEN_STATUS"]) is list:
            if len(model["DG"]["GEN_STATUS"]) != T:
                dg_info.GEN_STATUS.extend(model["DG"]["GEN_STATUS"] * T)
            else:
                dg_info.GEN_STATUS.extend(model["DG"]["GEN_STATUS"])
        elif type(model["UG"]["GEN_STATUS"]) is int:
            dg_info.GEN_STATUS.extend([model["UG"]["GEN_STATUS"]] * T)

        if type(model["DG"]["COMMAND_PG"]) is list:
            dg_info.PG.extend(model["DG"]["COMMAND_PG"])
        else:
            dg_info.PG.extend([model["DG"]["COMMAND_PG"]])

        if type(model["DG"]["COMMAND_RG"]) is list:
            dg_info.RG.extend(model["DG"]["COMMAND_RG"])
        else:
            dg_info.RG.extend([model["DG"]["COMMAND_RG"]])

        if type(model["DG"]["COMMAND_START_UP"]) is list:
            dg_info.COMMAND_STATUS.extend(model["DG"]["COMMAND_START_UP"])
        else:
            dg_info.COMMAND_STATUS.extend([model["DG"]["COMMAND_START_UP"]])

        dynamic_info.dg.extend([ug_info, dg_info])
        # Update ess part information
        ess_info.ID = 1
        ess_info.ESS_STATUS.extend([1]*T)
        if type(model["ESS"]["SOC"]) is list:
            ess_info.SOC.extend(model["ESS"]["SOC"])
        else:
            ess_info.SOC.extend([model["ESS"]["SOC"]])

        if type(model["ESS"]["COMMAND_PG"]) is list:
            ess_info.PG.extend(model["ESS"]["COMMAND_PG"])
        else:
            ess_info.PG.extend([model["ESS"]["COMMAND_PG"]])

        if type(model["ESS"]["COMMAND_RG"]) is list:
            ess_info.RG.extend(model["ESS"]["COMMAND_RG"])
        else:
            ess_info.RG.extend([model["ESS"]["COMMAND_RG"]])

        dynamic_info.ess.extend([ess_info])

        # Update pv part information
        pv_info.PG.extend(model["PV"]["PG"])
        if type(model["PV"]["COMMAND_CURT"]) is list:
            pv_info.COMMAND_CURT.extend(model["PV"]["COMMAND_CURT"])
        else:
            pv_info.COMMAND_CURT.extend([model["PV"]["COMMAND_CURT"]])
        dynamic_info.pv.extend([pv_info])

        # Update wp part information
        wp_info.PG.extend(model["WP"]["PG"])
        if type(model["WP"]["COMMAND_CURT"]) is list:
            wp_info.COMMAND_CURT.extend(model["WP"]["COMMAND_CURT"])
        else:
            wp_info.COMMAND_CURT.extend([model["WP"]["COMMAND_CURT"]])
        dynamic_info.wp.extend([wp_info])

        # Update load_ac part information
        load_ac_info.PD.extend(model["Load_ac"]["PD"])
        if type(model["Load_ac"]["COMMAND_SHED"]) is list:
            load_ac_info.COMMAND_SHED.extend(model["Load_ac"]["COMMAND_SHED"])
        else:
            load_ac_info.COMMAND_SHED.extend([model["Load_ac"]["COMMAND_SHED"]])

        load_uac_info.PD.extend(model["Load_uac"]["PD"])
        if type(model["Load_uac"]["COMMAND_SHED"]) is list:
            load_uac_info.COMMAND_SHED.extend(model["Load_uac"]["COMMAND_SHED"])
        else:
            load_uac_info.COMMAND_SHED.extend([model["Load_uac"]["COMMAND_SHED"]])

        dynamic_info.load_ac.extend([load_ac_info, load_uac_info])
        # Update load_dc part information
        load_dc_info.PD.extend(model["Load_dc"]["PD"])
        if type(model["Load_dc"]["COMMAND_SHED"]) is list:
            load_dc_info.COMMAND_SHED.extend(model["Load_dc"]["COMMAND_SHED"])
        else:
            load_dc_info.COMMAND_SHED.extend([model["Load_dc"]["COMMAND_SHED"]])

        load_udc_info.PD.extend(model["Load_udc"]["PD"])
        if type(model["Load_udc"]["COMMAND_SHED"]) is list:
            load_udc_info.COMMAND_SHED.extend(model["Load_udc"]["COMMAND_SHED"])
        else:
            load_udc_info.COMMAND_SHED.extend([model["Load_udc"]["COMMAND_SHED"]])

        dynamic_info.load_dc.extend([load_dc_info, load_udc_info])
        # Update convertor part information
        bic_info.STATUS.extend([1]*T)
        if type(model["BIC"]["COMMAND_AC2DC"]) is list:
            bic_info.PAC2DC.extend(model["BIC"]["COMMAND_AC2DC"])
        else:
            bic_info.PAC2DC.extend([model["BIC"]["COMMAND_AC2DC"]])

        if type(model["BIC"]["COMMAND_DC2AC"]) is list:
            bic_info.PDC2AC.extend(model["BIC"]["COMMAND_DC2AC"])
        else:
            bic_info.PDC2AC.extend([model["BIC"]["COMMAND_DC2AC"]])

        dynamic_info.bic.extend([bic_info])

        if type(model["PMG"]) is list:
            dynamic_info.PMG.extend(model["PMG"])
        else:
            dynamic_info.PMG.extend([model["PMG"]])
        dynamic_info.TIME_STAMP_COMMAND = Target_time

        return dynamic_info

    def info_extraction(*args):
        model = args[0]
        info = args[1]
        # The utility grid part
        model["UG"]["GEN_STATUS"] = info.dg[0].GEN_STATUS
        model["UG"]["COMMAND_PG"] = info.dg[0].PG
        # model["UG"]["COMMAND_SET_POINT_QG"] = info.dg[0].QG
        model["UG"]["COMMAND_RG"] = info.dg[0].RG
        # Update dg part information
        model["DG"]["GEN_STATUS"] = info.dg[1].GEN_STATUS
        model["DG"]["COMMAND_PG"] = info.dg[1].PG
        # model["DG"]["COMMAND_SET_POINT_QG"] = info.dg[1].QG
        model["DG"]["COMMAND_RG"] = info.dg[1].RG

        # Update ess part information
        model["ESS"]["COMMAND_PG"] = info.ess[0].PG
        model["ESS"]["SOC"] = info.ess[0].SOC
        # Update BIC part
        model["BIC"]["COMMAND_AC2DC"] = info.bic[0].PAC2DC
        model["BIC"]["COMMAND_DC2AC"] = info.bic[0].PDC2AC

        # Update pv part information
        model["PV"]["COMMAND_CURT"] = info.pv[0].COMMAND_CURT

        # Update wp part information
        model["WP"]["COMMAND_CURT"] = info.wp[0].COMMAND_CURT
        # Update load_ac part information
        model["Load_ac"]["COMMAND_SHED"] = info.load_ac[0].COMMAND_SHED
        model["Load_uac"]["COMMAND_SHED"] = info.load_ac[1].COMMAND_SHED

        model["Load_dc"]["COMMAND_SHED"] = info.load_dc[0].COMMAND_SHED
        model["Load_udc"]["COMMAND_SHED"] = info.load_dc[1].COMMAND_SHED

        model["PMG"] = info.PMG
        # model["V_DC"] = info.V_DC

        return model
