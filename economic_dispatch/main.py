"""
The alternating direction method of multipliers method is adopted in economic dispatch package
Jointed energy and reserves are optimized to reduce the operation cost.
Based on this method, the shadow price can also be calculated as well.
@author: Zhao Tianyang
@data: 18 September 2017
"""

import threading
import time
from configuration.configuration_time_line import default_time
from data_management.information_collection import Information_Collection_Thread
from data_management.information_management import information_formulation_extraction_dynamic
from data_management.information_management import information_receive_send
from economic_dispatch.mid_term_forecasting import ForecastingThread
from utils import Logger

logger_uems = Logger("Middle_term_dispatch_UEMS")
logger_lems = Logger("Middle_term_dispatch_LEMS")


class middle_term_operation():
    ##short term operation for ems
    # Two modes are proposed for the local ems and
    def middle_term_operation_uems(*args):
        # Short term forecasting for the middle term operation in universal energy management system.
        from data_management.database_management import database_operation
        from economic_dispatch.problem_formulation import problem_formulation
        from economic_dispatch.problem_solving import Solving_Thread
        from configuration.configuration_time_line import default_dead_line_time
        # Short term operation
        # General procedure for middle-term operation
        # 1)Information collection
        # 1.1)local EMS forecasting
        # 1.2)Information exchange
        universal_models = args[0]
        local_models = args[1]
        socket_upload = args[2]
        socket_download = args[3]
        info = args[4]
        session = args[5]

        Target_time = time.time()
        Target_time = round((Target_time - Target_time % default_time["Time_step_ed"] + default_time[
            "Time_step_ed"]))

        # Update the universal parameter by using the database engine
        # Two threads are created to obtain the information simultaneously.
        thread_forecasting = ForecastingThread(session, Target_time, universal_models)
        thread_info_ex = Information_Collection_Thread(socket_upload, info, local_models)

        thread_forecasting.start()
        thread_info_ex.start()

        thread_forecasting.join()
        thread_info_ex.join()

        universal_models = thread_forecasting.models
        local_models = thread_info_ex.local_models
        # Solve the optimal power flow problem
        # Two threads will be created, one for feasible problem, the other for infeasible problem
        mathematical_model = problem_formulation.problem_formulation_universal(local_models, universal_models,
                                                                               "Feasible")
        mathematical_model_recovery = problem_formulation.problem_formulation_universal(local_models, universal_models,
                                                                                        "Infeasible")
        # Solve the problem
        res = Solving_Thread(mathematical_model)
        res_recovery = Solving_Thread(mathematical_model_recovery)
        res.daemon = True
        res_recovery.daemon = True

        res.start()
        res_recovery.start()

        res.join(default_dead_line_time["Gate_closure_ed"])
        res_recovery.join(default_dead_line_time["Gate_closure_ed"])

        if res.value["success"] == True:
            (local_models, universal_models) = result_update(res.value, local_models, universal_models, "Feasible")
        else:
            (local_models, universal_models) = result_update(res_recovery.value, local_models, universal_models,
                                                             "Infeasible")

        # Return command to the local ems
        dynamic_model = information_formulation_extraction_dynamic.info_formulation(local_models, Target_time)
        dynamic_model.TIME_STAMP_COMMAND = round(time.time())

        information_send_thread = threading.Thread(target=information_receive_send.information_send,
                                                   args=(socket_upload, dynamic_model, 2))

        database_operation__uems = threading.Thread(target=database_operation.database_record,
                                                    args=(session, universal_models, Target_time, "ED"))
        logger_uems.info("The command for UEMS is {}".format(universal_models["PMG"]))
        information_send_thread.start()
        database_operation__uems.start()

        information_send_thread.join()
        database_operation__uems.join()

    def middle_term_operation_lems(*args):
        from data_management.database_management import database_operation
        # Short term operation for local ems
        # The following operation sequence
        # 1) Information collection
        # 2) Short-term forecasting
        # 3) Information upload and database store
        # 4) Download command and database operation
        local_models = args[0]  # Local energy management system models
        socket_upload = args[1]  # Upload information channel
        socket_download = args[2]  # Download information channel
        info = args[3]  # Information structure
        session = args[4]  # local database

        Target_time = time.time()
        Target_time = round((Target_time - Target_time % default_time["Time_step_ed"] + default_time[
            "Time_step_ed"]))

        # Step 1: Short-term forecasting
        thread_forecasting = ForecastingThread(session, Target_time, local_models)  # The forecasting thread
        thread_forecasting.start()
        thread_forecasting.join()

        local_models = thread_forecasting.models
        # Update the dynamic model
        dynamic_model = information_formulation_extraction_dynamic.info_formulation(local_models, Target_time, "ED")
        # Information send
        logger_lems.info("Sending request from {}".format(dynamic_model.AREA) + " to the serve")
        logger_lems.info("The local time is {}".format(dynamic_model.TIME_STAMP))
        information_receive_send.information_send(socket_upload, dynamic_model, 2)

        # Step2: Backup operation, which indicates the universal ems is down

        # Receive information from uems
        dynamic_model = information_receive_send.information_receive(socket_upload, info, 2)
        # print("The universal time is", dynamic_model.TIME_STAMP_COMMAND)
        logger_lems.info("The command from UEMS is {}".format(dynamic_model.PMG))
        # Store the data into the database

        local_models = information_formulation_extraction_dynamic.info_extraction(local_models, dynamic_model)

        database_operation.database_record(session, local_models, Target_time, "ED")


def result_update(*args):
    ## Result update for local ems and universal ems models
    from configuration.configuration_time_line import default_look_ahead_time_step
    res = args[0]
    local_model = args[1]
    universal_model = args[2]
    type = args[3]
    T = default_look_ahead_time_step["Look_ahead_time_ed_time_step"]

    if type == "Feasible":
        from modelling.power_flow.idx_ed_foramt import NX
    else:
        from modelling.power_flow.idx_ed_recovery_format import NX

    nx = T * NX
    x_local = res["x"][0:nx]  # Decouple of the solutions
    x_universal = res["x"][nx:2 * nx]

    local_model = update(x_local, local_model, type)
    universal_model = update(x_universal, universal_model, type)

    return local_model, universal_model


def update(*args):
    x = args[0]
    model = args[1]
    type = args[2]
    from configuration.configuration_time_line import default_look_ahead_time_step
    T = default_look_ahead_time_step["Look_ahead_time_ed_time_step"]

    if type == "Feasible":
        from modelling.power_flow.idx_ed_foramt import PG, RG, PUG, RUG, PBIC_AC2DC, PBIC_DC2AC, PESS_C, PESS_DC, RESS, \
            PMG, NX
        model["DG"]["COMMAND_PG"] = [0] * T
        model["DG"]["COMMAND_RG"] = [0] * T
        model["UG"]["COMMAND_PG"] = [0] * T
        model["UG"]["COMMAND_RG"] = [0] * T
        model["BIC"]["COMMAND_AC2DC"] = [0] * T
        model["BIC"]["COMMAND_DC2AC"] = [0] * T
        model["ESS"]["COMMAND_PG"] = [0] * T
        model["ESS"]["COMMAND_RG"] = [0] * T
        for i in range(T):
            model["DG"]["COMMAND_PG"][i] = x[i * NX + PG]
            model["DG"]["COMMAND_RG"][i] = x[i * NX + RG]

            model["UG"]["COMMAND_PG"][i] = x[i * NX + PUG]
            model["UG"]["COMMAND_RG"][i] = x[i * NX + RUG]

            model["BIC"]["COMMAND_AC2DC"][i] = x[i * NX + PBIC_AC2DC]
            model["BIC"]["COMMAND_DC2AC"][i] = x[i * NX + PBIC_DC2AC]

            model["ESS"]["COMMAND_PG"][i] = x[i * NX + PESS_DC] - x[i * NX + PESS_C]
            model["ESS"]["COMMAND_RG"][i] = x[i * NX + RESS]

            model["PMG"][i] = x[i * NX + PMG]
    else:
        from modelling.power_flow.idx_ed_recovery_format import PG, RG, PUG, RUG, PBIC_AC2DC, PBIC_DC2AC, PESS_C, \
            PESS_DC, RESS, PMG, PPV, PWP, PL_AC, PL_UAC, PL_DC, PL_UDC, NX

        model["DG"]["COMMAND_PG"] = [0] * T
        model["DG"]["COMMAND_RG"] = [0] * T
        model["UG"]["COMMAND_PG"] = [0] * T
        model["UG"]["COMMAND_RG"] = [0] * T
        model["BIC"]["COMMAND_AC2DC"] = [0] * T
        model["BIC"]["COMMAND_DC2AC"] = [0] * T
        model["ESS"]["COMMAND_PG"] = [0] * T
        model["ESS"]["COMMAND_RG"] = [0] * T
        model["PV"]["COMMAND_CURT"] = [0] * T
        model["WP"]["COMMAND_CURT"] = [0] * T

        model["Load_ac"]["COMMAND_SHED"] = [0] * T
        model["Load_uac"]["COMMAND_SHED"] = [0] * T
        model["Load_dc"]["COMMAND_SHED"] = [0] * T
        model["Load_udc"]["COMMAND_SHED"] = [0] * T
        for i in range(T):
            model["DG"]["COMMAND_PG"][i] = x[i * NX + PG]
            model["DG"]["COMMAND_RG"][i] = x[i * NX + RG]

            model["UG"]["COMMAND_PG"][i] = x[i * NX + PUG]
            model["UG"]["COMMAND_RG"][i] = x[i * NX + RUG]

            model["BIC"]["COMMAND_AC2DC"][i] = x[i * NX + PBIC_AC2DC]
            model["BIC"]["COMMAND_DC2AC"][i] = x[i * NX + PBIC_DC2AC]

            model["ESS"]["COMMAND_PG"][i] = x[i * NX + PESS_DC] - x[i * NX + PESS_C]
            model["ESS"]["COMMAND_RG"][i] = x[i * NX + RESS]

            model["PMG"][i] = x[i * NX + PMG]

            model["PV"]["COMMAND_CURT"][i] = min(model["PV"]["PG"], x[i * NX + PPV])
            model["WP"]["COMMAND_CURT"] = min(model["WP"]["PG"], x[i * NX + PWP])

            model["Load_ac"]["COMMAND_SHED"] = min(model["Load_ac"]["PD"], x[i * NX + PL_AC])
            model["Load_uac"]["COMMAND_SHED"] = min(model["Load_uac"]["PD"], x[i * NX + PL_UAC])
            model["Load_dc"]["COMMAND_SHED"] = min(model["Load_dc"]["PD"], x[i * NX + PL_DC])
            model["Load_udc"]["COMMAND_SHED"] = min(model["Load_udc"]["PD"], x[i * NX + PL_UDC])

    return model
