"""
Jointed energy and reserves are optimized to reduce the operation cost and risk.
@author: Zhao Tianyang
@data: 21 September 2017
"""

import threading
import time
from configuration.configuration_time_line import default_time,default_look_ahead_time_step
from data_management.information_collection import Information_Collection_Thread
from data_management.information_management import information_formulation_extraction_dynamic
from data_management.information_management import information_receive_send
from unit_commitment.long_tertm_forecasting import ForecastingThread
from utils import Logger
from copy import deepcopy
from unit_commitment.input_check import input_check_long_term
from unit_commitment.output_check import output_local_check
from unit_commitment.long2middle import long2middle_opeartion
logger_uems = Logger("Long_term_dispatch_UEMS")
logger_lems = Logger("Long_term_dispatch_LEMS")

class long_term_operation():
    ##short term operation for ems
    # Two modes are proposed for the local ems and
    def long_term_operation_uems(*args):
        # Short term forecasting for the middle term operation in universal energy management system.
        from data_management.database_management import database_operation
        from unit_commitment.problem_formulation import problem_formulation
        from unit_commitment.problem_solving import Solving_Thread
        from configuration.configuration_time_line import default_dead_line_time
        # Short term operation
        # General procedure for middle-term operation
        # 1)Information collection
        # 1.1)local EMS forecasting
        # 1.2)Information exchange
        universal_models = deepcopy(args[0])
        local_models = deepcopy(args[1])
        socket_upload = args[2]
        socket_download = args[3]
        info = args[4]
        session = args[5]

        Target_time = time.time()
        Target_time = round((Target_time - Target_time % default_time["Time_step_uc"] + default_time["Time_step_uc"]))

        # Update the universal parameter by using the database engine
        # Two threads are created to obtain the information simultaneously.
        thread_forecasting = ForecastingThread(session, Target_time, universal_models)
        thread_info_ex = Information_Collection_Thread(socket_upload, info, local_models,default_look_ahead_time_step["Look_ahead_time_uc_time_step"])

        thread_forecasting.start()
        thread_info_ex.start()

        thread_forecasting.join()
        thread_info_ex.join()

        universal_models = thread_forecasting.models
        local_models = thread_info_ex.local_models

        local_models = input_check_long_term.model_local_check(local_models)
        universal_models = input_check_long_term.model_universal_check(universal_models)
        # Solve the optimal power flow problem
        # Two threads will be created, one for feasible problem, the other for infeasible problem
        # universal_models["ESS"]["SOC"]=universal_models["ESS"]["SOC_MIN"], the test shows that, the input check is necessary.

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

        res.join(default_dead_line_time["Gate_closure_uc"])
        res_recovery.join(default_dead_line_time["Gate_closure_uc"])

        if res.value["success"] == True:
            (local_models, universal_models) = result_update(res.value, local_models, universal_models, "Feasible")
        else:
            (local_models, universal_models) = result_update(res_recovery.value, local_models, universal_models,
                                                             "Infeasible")

        local_models = output_local_check(local_models)
        universal_models = output_local_check(universal_models)

        # Return command to the local ems
        local_models["COMMAND_TYPE"] = 0
        dynamic_model = information_formulation_extraction_dynamic.info_formulation(local_models, Target_time,"UC")
        dynamic_model.TIME_STAMP_COMMAND = round(time.time())

        information_send_thread = threading.Thread(target=information_receive_send.information_send,
                                                   args=(socket_upload, dynamic_model, 2))

        database_operation_uems = threading.Thread(target=database_operation.database_record,
                                                    args=(session, universal_models, Target_time, "UC"))

        long2middle_opeartion(Target_time, session, universal_models)
        logger_uems.info("The command for UEMS is {}".format(universal_models["PMG"]))
        information_send_thread.start()
        database_operation_uems.start()

        information_send_thread.join()
        database_operation_uems.join()

    def long_term_operation_lems(*args):
        from data_management.database_management import database_operation
        # Short term operation for local ems
        # The following operation sequence
        # 1) Information collection
        # 2) Short-term forecasting
        # 3) Information upload and database store
        # 4) Download command and database operation
        local_models = deepcopy(args[0])  # Local energy management system models
        socket_upload = args[1]  # Upload information channel
        socket_download = args[2]  # Download information channel
        info = args[3]  # Information structure
        session = args[4]  # local database

        Target_time = time.time()
        Target_time = round((Target_time - Target_time % default_time["Time_step_uc"] + default_time[
            "Time_step_uc"]))

        # Step 1: Short-term forecasting
        thread_forecasting = ForecastingThread(session, Target_time, local_models)  # The forecasting thread
        thread_forecasting.start()
        thread_forecasting.join()

        local_models = thread_forecasting.models
        # Update the dynamic model
        local_models["COMMAND_TYPE"] = 0
        dynamic_model = information_formulation_extraction_dynamic.info_formulation(local_models, Target_time,"UC")
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

        long2middle_opeartion(Target_time, session, local_models)

        database_operation_lems = threading.Thread(target=database_operation.database_record,
                                                    args=(session, local_models, Target_time, "UC"))

        database_operation_lems.start()
        database_operation_lems.join()


def result_update(*args):
    ## Result update for local ems and universal ems models
    res = args[0]
    local_model = args[1]
    universal_model = args[2]
    type = args[3]
    T = default_look_ahead_time_step["Look_ahead_time_uc_time_step"]

    if type == "Feasible":
        from modelling.power_flow.idx_uc_format import NX
    else:
        from modelling.power_flow.idx_uc_recovery_format import NX

    nx = T * NX
    x_local = res["x"][0:nx]
    x_universal = res["x"][nx:2*nx]

    local_model = update(x_local, local_model, type)
    universal_model = update(x_universal, universal_model, type)

    return local_model, universal_model


def update(*args):
    x = args[0]
    model = args[1]
    type = args[2]

    T = default_look_ahead_time_step["Look_ahead_time_uc_time_step"]

    if type == "Feasible":
        from modelling.power_flow.idx_uc_format import IG, PG, RG, IUG, PUG, RUG, PBIC_AC2DC, PBIC_DC2AC, PESS_C, PESS_DC, RESS,EESS,\
            PMG, NX
        model["DG"]["COMMAND_START_UP"] = [0] * T
        model["DG"]["COMMAND_PG"] = [0] * T
        model["DG"]["COMMAND_RG"] = [0] * T

        model["UG"]["COMMAND_START_UP"] = [0] * T
        model["UG"]["COMMAND_PG"] = [0] * T
        model["UG"]["COMMAND_RG"] = [0] * T

        model["BIC"]["COMMAND_AC2DC"] = [0] * T
        model["BIC"]["COMMAND_DC2AC"] = [0] * T

        model["ESS"]["COMMAND_PG"] = [0] * T
        model["ESS"]["COMMAND_RG"] = [0] * T
        model["ESS"]["SOC"] = [0]*T

        model["PV"]["COMMAND_CURT"] = [0] * T
        model["WP"]["COMMAND_CURT"] = [0] * T

        model["PMG"] = [0] * T

        model["Load_ac"]["COMMAND_SHED"] = [0] * T
        model["Load_uac"]["COMMAND_SHED"] = [0] * T
        model["Load_dc"]["COMMAND_SHED"] = [0] * T
        model["Load_udc"]["COMMAND_SHED"] = [0] * T

        for i in range(T):
            model["DG"]["COMMAND_START_UP"][i] = int(x[i * NX + IG])
            model["DG"]["COMMAND_PG"][i] = int(x[i * NX + PG])
            model["DG"]["COMMAND_RG"][i] = int(x[i * NX + RG])

            model["UG"]["COMMAND_START_UP"][i] = int(x[i * NX + IUG])
            model["UG"]["COMMAND_PG"][i] = int(x[i * NX + PUG])
            model["UG"]["COMMAND_RG"][i] = int(x[i * NX + RUG])

            model["BIC"]["COMMAND_AC2DC"][i] = int(x[i * NX + PBIC_AC2DC])
            model["BIC"]["COMMAND_DC2AC"][i] = int(x[i * NX + PBIC_DC2AC])

            model["ESS"]["COMMAND_PG"][i] = int(x[i * NX + PESS_DC] - x[i * NX + PESS_C])
            model["ESS"]["COMMAND_RG"][i] = int(x[i * NX + RESS])
            model["ESS"]["SOC"][i] = x[i*NX+EESS]/model["ESS"]["CAP"]

            model["PMG"][i] = int(x[i * NX + PMG])

        model["success"] = True
    else:
        from modelling.power_flow.idx_uc_recovery_format import IG, PG, RG, IUG, PUG, RUG, PBIC_AC2DC, PBIC_DC2AC, PESS_C,EESS, \
            PESS_DC, RESS, PMG, PPV, PWP, PL_AC, PL_UAC, PL_DC, PL_UDC, NX

        model["DG"]["COMMAND_START_UP"] = [0] * T
        model["DG"]["COMMAND_PG"] = [0] * T
        model["DG"]["COMMAND_RG"] = [0] * T

        model["UG"]["COMMAND_START_UP"] = [0] * T
        model["UG"]["COMMAND_PG"] = [0] * T
        model["UG"]["COMMAND_RG"] = [0] * T

        model["BIC"]["COMMAND_AC2DC"] = [0] * T
        model["BIC"]["COMMAND_DC2AC"] = [0] * T

        model["ESS"]["COMMAND_PG"] = [0] * T
        model["ESS"]["COMMAND_RG"] = [0] * T
        model["ESS"]["SOC"] = [0] * T

        model["PV"]["COMMAND_CURT"] = [0] * T
        model["WP"]["COMMAND_CURT"] = [0] * T

        model["PMG"] = [0] * T

        model["Load_ac"]["COMMAND_SHED"] = [0] * T
        model["Load_uac"]["COMMAND_SHED"] = [0] * T
        model["Load_dc"]["COMMAND_SHED"] = [0] * T
        model["Load_udc"]["COMMAND_SHED"] = [0] * T

        for i in range(T):
            # Update the solutions
            model["DG"]["COMMAND_START_UP"][i] = int(x[i * NX + IG])
            model["DG"]["COMMAND_PG"][i] = int(x[i * NX + PG])
            model["DG"]["COMMAND_RG"][i] = int(x[i * NX + RG])

            model["UG"]["COMMAND_START_UP"][i] = int(x[i * NX + IUG])
            model["UG"]["COMMAND_PG"][i] = int(x[i * NX + PUG])
            model["UG"]["COMMAND_RG"][i] = int(x[i * NX + RUG])

            model["BIC"]["COMMAND_AC2DC"][i] = int(x[i * NX + PBIC_AC2DC])
            model["BIC"]["COMMAND_DC2AC"][i] = int(x[i * NX + PBIC_DC2AC])

            model["ESS"]["COMMAND_PG"][i] = int(x[i * NX + PESS_DC] - x[i * NX + PESS_C])
            model["ESS"]["COMMAND_RG"][i] = int(x[i * NX + RESS])
            model["ESS"]["SOC"][i] = x[i * NX + EESS]/model["ESS"]["CAP"]

            model["PMG"][i] = int(x[i * NX + PMG])

            model["PV"]["COMMAND_CURT"][i] = int(x[i * NX + PPV])
            model["WP"]["COMMAND_CURT"][i] = int(x[i * NX + PWP])

            model["Load_ac"]["COMMAND_SHED"][i] = int(x[i * NX + PL_AC])
            model["Load_uac"]["COMMAND_SHED"][i] = int(x[i * NX + PL_UAC])
            model["Load_dc"]["COMMAND_SHED"][i] = int(x[i * NX + PL_DC])
            model["Load_udc"]["COMMAND_SHED"][i] = int(x[i * NX + PL_UDC])

        model["success"] = False
    return model