# Problem formulation for the set-points tracing method
from numpy import array, vstack, zeros
import numpy
from utils import Logger
from copy import deepcopy
from configuration.configuration_eps import default_eps
logger = Logger("Set-points Tracing Problem formulation for UEMS")

class problem_formulation_tracing():
    ## Reformulte the information model to system level
    def problem_formulation_local(*args):
        from configuration import configuration_time_line
        from modelling.power_flow.idx_ed_set_points_tracing import PG, RG, PUG, RUG, PBIC_AC2DC, PBIC_DC2AC, PESS_C, \
            PESS_DC, RESS, EESS, PMG, PMG_negative, PMG_positive, PUG_negative, PUG_positive, SOC_negative, \
            SOC_positive, NX
        model = deepcopy(args[0])  # If multiple models are inputed, more local ems models will be formulated
        ## The feasible optimal problem formulation
        T = configuration_time_line.default_look_ahead_time_step["Look_ahead_time_ed_time_step"]
        nx = NX * T

        lb = [0] * NX
        ub = [0] * NX
        ## Update lower boundary
        lb[PG] = model["DG"]["PMIN"]
        lb[RG] = model["DG"]["PMIN"]

        lb[PUG] = model["UG"]["PMIN"]
        lb[RUG] = model["UG"]["PMIN"]

        lb[PBIC_AC2DC] = 0
        lb[PBIC_DC2AC] = 0

        lb[PESS_C] = 0
        lb[PESS_DC] = 0
        lb[RESS] = 0
        lb[EESS] = model["ESS"]["SOC_MIN"] * model["ESS"]["CAP"]

        lb[PMG] = 0  # The line flow limitation, the predefined status is, the transmission line is off-line

        lb[PMG_negative] = 0
        lb[PMG_positive] = 0
        lb[PUG_positive] = 0
        lb[PUG_negative] = 0
        lb[SOC_positive] = 0
        lb[SOC_negative] = 0
        ## Update lower boundary
        ub[PG] = model["DG"]["PMAX"]
        ub[RG] = model["DG"]["PMAX"]

        ub[PUG] = model["UG"]["PMAX"]
        ub[RUG] = model["UG"]["PMAX"]

        ub[PBIC_AC2DC] = model["BIC"]["CAP"]
        ub[PBIC_DC2AC] = model["BIC"]["CAP"]

        ub[PESS_C] = model["ESS"]["PMAX_CH"]
        ub[PESS_DC] = model["ESS"]["PMAX_DIS"]
        ub[RESS] = model["ESS"]["PMAX_DIS"] + model["ESS"]["PMAX_CH"]
        ub[EESS] = model["ESS"]["SOC_MAX"] * model["ESS"]["CAP"]

        ub[PMG] = 0  # The line flow limitation, the predefined status is, the transmission line is off-line
        ub[PMG_positive] = 0  # This boundary information will ne updated to the
        ub[PMG_negative] = 0
        ub[PUG_positive] = model["UG"]["PMAX"]
        ub[PUG_negative] = model["UG"]["PMAX"]
        ub[SOC_positive] = model["ESS"]["PMAX_DIS"] + model["ESS"]["PMAX_CH"]  # The up relaxation of SOC, this is
        ub[SOC_negative] = model["ESS"]["PMAX_DIS"] + model["ESS"]["PMAX_CH"]  # The up relaxation of SOC
        # Finalize the boundary information
        LB = lb * T
        UB = ub * T

        ## Constraints set
        # 1) Power balance equation
        Aeq = zeros((T, nx))
        beq = []
        for i in range(T):
            Aeq[i][i * NX + PG] = 1
            Aeq[i][i * NX + PUG] = 1
            Aeq[i][i * NX + PBIC_AC2DC] = -1
            Aeq[i][i * NX + PBIC_DC2AC] = model["BIC"]["EFF_DC2AC"]
            beq.append(model["Load_ac"]["PD"][i] + model["Load_uac"]["PD"][i])

        # 2) DC power balance equation
        Aeq_temp = zeros((T, nx))
        for i in range(T):
            Aeq_temp[i][i * NX + PBIC_AC2DC] = model["BIC"]["EFF_AC2DC"]
            Aeq_temp[i][i * NX + PBIC_DC2AC] = -1
            Aeq_temp[i][i * NX + PESS_C] = -1
            Aeq_temp[i][i * NX + PESS_DC] = 1
            Aeq_temp[i][i * NX + PMG] = -1
            beq.append(
                model["Load_dc"]["PD"][i] + model["Load_udc"]["PD"][i] - model["PV"]["PG"][i] - model["WP"]["PG"][i])

        Aeq = vstack([Aeq, Aeq_temp])

        # 3) Energy storage system
        Aeq_temp = zeros((T, nx))
        for i in range(T):
            if i == 0:
                Aeq_temp[i][i * NX + EESS] = 1
                Aeq_temp[i][i * NX + PESS_C] = -model["ESS"]["EFF_CH"] * configuration_time_line.default_time[
                    "Time_step_ed"] / 3600
                Aeq_temp[i][i * NX + PESS_DC] = 1 / model["ESS"]["EFF_DIS"] * configuration_time_line.default_time[
                    "Time_step_ed"] / 3600
                beq.append(model["ESS"]["SOC"] * model["ESS"]["CAP"])

            else:
                Aeq_temp[i][(i - 1) * NX + EESS] = -1
                Aeq_temp[i][i * NX + EESS] = 1
                Aeq_temp[i][i * NX + PESS_C] = -model["ESS"]["EFF_CH"] * configuration_time_line.default_time[
                    "Time_step_ed"] / 3600
                Aeq_temp[i][i * NX + PESS_DC] = 1 / model["ESS"]["EFF_DIS"] * configuration_time_line.default_time[
                    "Time_step_ed"] / 3600
                beq.append(0)
        Aeq = vstack([Aeq, Aeq_temp])
        # Inequality constraints
        # 1) PG + RG <= PGMAX
        Aineq = zeros((T, nx))
        bineq = []
        for i in range(T):
            Aineq[i][i * NX + PG] = 1
            Aineq[i][i * NX + RG] = 1
            bineq.append(model["DG"]["PMAX"])
        # 2) PG - RG >= PGMIN
        Aineq_temp = zeros((T, nx))
        for i in range(T):
            Aineq_temp[i][i * NX + PG] = -1
            Aineq_temp[i][i * NX + RG] = 1
            bineq.append(-model["DG"]["PMIN"])
        Aineq = vstack([Aineq, Aineq_temp])
        # 3) PUG + RUG <= PUGMAX
        Aineq_temp = zeros((T, nx))
        for i in range(T):
            Aineq_temp[i][i * NX + PUG] = 1
            Aineq_temp[i][i * NX + RUG] = 1
            bineq.append(model["UG"]["PMAX"])
        Aineq = vstack([Aineq, Aineq_temp])
        # 4) PUG - RUG >= PUGMIN
        Aineq_temp = zeros((T, nx))
        for i in range(T):
            Aineq_temp[i][i * NX + PUG] = -1
            Aineq_temp[i][i * NX + RUG] = 1
            bineq.append(-model["UG"]["PMIN"])
        Aineq = vstack([Aineq, Aineq_temp])
        # 5) PESS_DC - PESS_C + RESS <= PESS_DC_MAX
        Aineq_temp = zeros((T, nx))
        for i in range(T):
            Aineq_temp[i][i * NX + PESS_DC] = 1
            Aineq_temp[i][i * NX + PESS_C] = -1
            Aineq_temp[i][i * NX + RESS] = 1
            bineq.append(model["ESS"]["PMAX_DIS"])
        Aineq = vstack([Aineq, Aineq_temp])
        # 6) PESS_DC - PESS_C - RESS >= -PESS_C_MAX
        Aineq_temp = zeros((T, nx))
        for i in range(T):
            Aineq_temp[i][i * NX + PESS_DC] = -1
            Aineq_temp[i][i * NX + PESS_C] = 1
            Aineq_temp[i][i * NX + RESS] = 1
            bineq.append(model["ESS"]["PMAX_CH"])
        Aineq = vstack([Aineq, Aineq_temp])
        # 7) EESS - RESS*delta >= EESSMIN
        Aineq_temp = zeros((T, nx))
        for i in range(T):
            Aineq_temp[i][i * NX + EESS] = -1
            Aineq_temp[i][i * NX + RESS] = configuration_time_line.default_time["Time_step_ed"] / 3600
            bineq.append(-model["ESS"]["SOC_MIN"] * model["ESS"]["CAP"])
        Aineq = vstack([Aineq, Aineq_temp])
        # 8) EESS + RESS*delta <= EESSMAX
        Aineq_temp = zeros((T, nx))
        for i in range(T):
            Aineq_temp[i][i * NX + EESS] = 1
            Aineq_temp[i][i * NX + RESS] = configuration_time_line.default_time["Time_step_ed"] / 3600
            bineq.append(model["ESS"]["SOC_MAX"] * model["ESS"]["CAP"])
        Aineq = vstack([Aineq, Aineq_temp])
        # 9) RG + RUG + RESS >= sum(Load)*beta + sum(PV)*beta_pv + sum(WP)*beta_wp
        # No reserve requirement
        # 10) PUG-PUG_positive<=PUG_SET_POINT
        Aineq_temp = zeros((T, nx))
        for i in range(T):
            Aineq_temp[i][i * NX + PUG] = 1
            Aineq_temp[i][i * NX + PUG_positive] = -1
            bineq.append(model["UG"]["COMMAND_PG"][i])
        # 11) PUG+PUG_negative>=PUG_SET_POINT
        Aineq_temp = zeros((T, nx))
        for i in range(T):
            Aineq_temp[i][i * NX + PUG] = -1
            Aineq_temp[i][i * NX + PUG_negative] = -1
            bineq.append(-model["UG"]["COMMAND_PG"][i])
        # 12) PMG-PMG_positive<=PMG_SET_POINT
        Aineq_temp = zeros((T, nx))
        for i in range(T):
            Aineq_temp[i][i * NX + PMG] = 1
            Aineq_temp[i][i * NX + PMG_positive] = -1
            bineq.append(model["PMG"][i])
        # 13) PMG+PMG_negative>=PMG_SET_POINT
        Aineq_temp = zeros((T, nx))
        for i in range(T):
            Aineq_temp[i][i * NX + PMG] = -1
            Aineq_temp[i][i * NX + PMG_negative] = -1
            bineq.append(-model["PMG"][i])
        # 14) PESS_DC-PESS_C-SOC_positve<=PESS_SET_POINT
        Aineq_temp = zeros((T, nx))
        for i in range(T):
            Aineq_temp[i][i * NX + PESS_DC] = 1
            Aineq_temp[i][i * NX + PESS_C] = -1
            Aineq_temp[i][i * NX + SOC_positive] = -1
            bineq.append(model["ESS"]["COMMAND_PG"][i])
        # 15) PESS_DC-PESS_C+SOC_negative>=PESS_SET_POINT
        Aineq_temp = zeros((T, nx))
        for i in range(T):
            Aineq_temp[i][i * NX + PESS_DC] = -1
            Aineq_temp[i][i * NX + PESS_C] = 1
            Aineq_temp[i][i * NX + SOC_positive] = -1
            bineq.append(-model["ESS"]["COMMAND_PG"][i])

        c = [0] * NX
        if model["DG"]["COST_MODEL"] == 2:
            c[PG] = model["DG"]["COST"][1]
        else:
            c[PG] = model["DG"]["COST"][0]
        c[PUG] = model["UG"]["COST"][0]
        c[PESS_C] = model["ESS"]["COST_CH"][0]
        c[PESS_DC] = model["ESS"]["COST_DIS"][0]
        c[PMG_negative] = default_eps["Penalty_ed"]
        c[PMG_positive] = default_eps["Penalty_ed"]
        c[PUG_positive] = default_eps["Penalty_ed"]
        c[PUG_negative] = default_eps["Penalty_ed"]
        c[SOC_positive] = default_eps["Penalty_ed"]
        c[SOC_negative] = default_eps["Penalty_ed"]
        c[PBIC_AC2DC] = default_eps["Penalty_ed"] / 10  # These two items are added to remove the bilinear constraints :1)
        c[PBIC_DC2AC] = default_eps["Penalty_ed"] / 10  # 2)

        C = c * T
        # Generate the quadratic parameters
        Q = zeros((nx, nx))
        for i in range(T):
            if model["DG"]["COST_MODEL"] == 2:
                Q[i * NX + PG][i * NX + PG] = model["DG"]["COST"][1]

        mathematical_model = {"Q": Q,
                              "c": C,
                              "Aeq": Aeq,
                              "beq": beq,
                              "A": Aineq,
                              "b": bineq,
                              "lb": LB,
                              "ub": UB}

        return mathematical_model

    def problem_formulation_local_recovery(*args):
        from configuration import configuration_time_line
        from modelling.power_flow.idx_ed_set_points_tracing_recovery import PG, RG, PUG, RUG, PBIC_AC2DC, PBIC_DC2AC, \
            PESS_C, PESS_DC, RESS, EESS, PMG, PPV, PWP, PL_AC, PL_UAC, PL_DC, PL_UDC, PMG_negative, PMG_positive, PUG_negative, PUG_positive, SOC_negative, SOC_positive, NX

        model = deepcopy(args[0])  # If multiple models are inputed, more local ems models will be formulated
        ## The infeasible optimal problem formulation
        T = configuration_time_line.default_look_ahead_time_step["Look_ahead_time_ed_time_step"]
        nx = T * NX
        lb = [0] * nx
        ub = [0] * nx

        for i in range(T):
            ## Update lower boundary
            lb[i * NX + PG] = model["DG"]["PMIN"]
            lb[i * NX + RG] = model["DG"]["PMIN"]
            lb[i * NX + PUG] = model["UG"]["PMIN"]
            lb[i * NX + RUG] = model["UG"]["PMIN"]
            lb[i * NX + PBIC_AC2DC] = 0
            lb[i * NX + PBIC_DC2AC] = 0
            lb[i * NX + PESS_C] = 0
            lb[i * NX + PESS_DC] = 0
            lb[i * NX + RESS] = 0
            lb[i * NX + EESS] = model["ESS"]["SOC_MIN"] * model["ESS"]["CAP"]
            lb[
                i * NX + PMG] = 0  # The line flow limitation, the predefined status is, the transmission line is off-line
            lb[i * NX + PPV] = 0
            lb[i * NX + PWP] = 0
            lb[i * NX + PL_AC] = 0
            lb[i * NX + PL_UAC] = 0
            lb[i * NX + PL_DC] = 0
            lb[i * NX + PL_UDC] = 0
            lb[i * NX + PMG_negative] = 0
            lb[i * NX + PMG_positive] = 0
            lb[i * NX + PUG_positive] = 0
            lb[i * NX + PUG_negative] = 0
            lb[i * NX + SOC_positive] = 0
            lb[i * NX + SOC_negative] = 0
            ## Update lower boundary
            ub[i * NX + PG] = model["DG"]["PMAX"]
            ub[i * NX + RG] = model["DG"]["PMAX"]
            ub[i * NX + PUG] = model["UG"]["PMAX"]
            ub[i * NX + RUG] = model["UG"]["PMAX"]
            ub[i * NX + PBIC_AC2DC] = model["BIC"]["CAP"]
            ub[i * NX + PBIC_DC2AC] = model["BIC"]["CAP"]
            ub[i * NX + PESS_C] = model["ESS"]["PMAX_CH"]
            ub[i * NX + PESS_DC] = model["ESS"]["PMAX_DIS"]
            ub[i * NX + RESS] = model["ESS"]["PMAX_DIS"] + model["ESS"]["PMAX_CH"]
            ub[i * NX + EESS] = model["ESS"]["SOC_MAX"] * model["ESS"]["CAP"]
            ub[i * NX + PMG] = 0  # The line flow limitation, the predefined status is, the transmission line is off-line
            ub[i * NX + PPV] = model["PV"]["PG"][i]
            ub[i * NX + PWP] = model["WP"]["PG"][i]
            ub[i * NX + PL_AC] = model["Load_ac"]["PD"][i]
            ub[i * NX + PL_UAC] = model["Load_uac"]["PD"][i]
            ub[i * NX + PL_DC] = model["Load_dc"]["PD"][i]
            ub[i * NX + PL_UDC] = model["Load_udc"]["PD"][i]
            ub[i * NX + PMG_positive] = 0  # This boundary information will ne updated to the
            ub[i * NX + PMG_negative] = 0
            ub[i * NX + PUG_positive] = model["UG"]["PMAX"]
            ub[i * NX + PUG_negative] = model["UG"]["PMAX"]
            ub[i * NX + SOC_positive] = model["ESS"]["PMAX_DIS"] + model["ESS"]["PMAX_CH"]  # The up relaxation of SOC, this is
            ub[i * NX + SOC_negative] = model["ESS"]["PMAX_DIS"] + model["ESS"]["PMAX_CH"]  # The up relaxation of SOC

        ## Constraints set
        # 1) Power balance equation
        Aeq = zeros((T, nx))
        beq = []
        for i in range(T):
            Aeq[i][i * NX + PG] = 1
            Aeq[i][i * NX + PUG] = 1
            Aeq[i][i * NX + PBIC_AC2DC] = -1
            Aeq[i][i * NX + PBIC_DC2AC] = model["BIC"]["EFF_DC2AC"]
            Aeq[i][i * NX + PL_AC] = -1
            Aeq[i][i * NX + PL_UAC] = -1
            beq.append(0)
        # 2) DC power balance equation
        Aeq_temp = zeros((T, nx))
        for i in range(T):
            Aeq_temp[i][i * NX + PBIC_AC2DC] = model["BIC"]["EFF_AC2DC"]
            Aeq_temp[i][i * NX + PBIC_DC2AC] = -1
            Aeq_temp[i][i * NX + PESS_C] = -1
            Aeq_temp[i][i * NX + PESS_DC] = 1
            Aeq_temp[i][i * NX + PMG] = -1
            Aeq_temp[i][i * NX + PL_DC] = -1
            Aeq_temp[i][i * NX + PL_UDC] = -1
            Aeq_temp[i][i * NX + PPV] = 1
            Aeq_temp[i][i * NX + PWP] = 1
            beq.append(0)
        Aeq = vstack([Aeq, Aeq_temp])

        # 3) Energy storage system
        Aeq_temp = zeros((T, nx))
        for i in range(T):
            if i == 0:
                Aeq_temp[i][i * NX + EESS] = 1
                Aeq_temp[i][i * NX + PESS_C] = -model["ESS"]["EFF_CH"] * configuration_time_line.default_time[
                    "Time_step_ed"] / 3600
                Aeq_temp[i][i * NX + PESS_DC] = 1 / model["ESS"]["EFF_DIS"] * configuration_time_line.default_time[
                    "Time_step_ed"] / 3600
                beq.append(model["ESS"]["SOC"] * model["ESS"]["CAP"])

            else:
                Aeq_temp[i][(i - 1) * NX + EESS] = -1
                Aeq_temp[i][i * NX + EESS] = 1
                Aeq_temp[i][i * NX + PESS_C] = -model["ESS"]["EFF_CH"] * configuration_time_line.default_time[
                    "Time_step_ed"] / 3600
                Aeq_temp[i][i * NX + PESS_DC] = 1 / model["ESS"]["EFF_DIS"] * configuration_time_line.default_time[
                    "Time_step_ed"] / 3600
                beq.append(0)
        Aeq = vstack([Aeq, Aeq_temp])

        # Inequality constraints
        # Inequality constraints
        # 1) PG + RG <= PGMAX
        Aineq = zeros((T, nx))
        bineq = []
        for i in range(T):
            Aineq[i][i * NX + PG] = 1
            Aineq[i][i * NX + RG] = 1
            bineq.append(model["DG"]["PMAX"])
        # 2) PG - RG >= PGMIN
        Aineq_temp = zeros((T, nx))
        for i in range(T):
            Aineq_temp[i][i * NX + PG] = -1
            Aineq_temp[i][i * NX + RG] = 1
            bineq.append(-model["DG"]["PMIN"])
        Aineq = vstack([Aineq, Aineq_temp])
        # 3) PUG + RUG <= PUGMAX
        Aineq_temp = zeros((T, nx))
        for i in range(T):
            Aineq_temp[i][i * NX + PUG] = 1
            Aineq_temp[i][i * NX + RUG] = 1
            bineq.append(model["UG"]["PMAX"])
        Aineq = vstack([Aineq, Aineq_temp])
        # 4) PUG - RUG >= PUGMIN
        Aineq_temp = zeros((T, nx))
        for i in range(T):
            Aineq_temp[i][i * NX + PUG] = -1
            Aineq_temp[i][i * NX + RUG] = 1
            bineq.append(-model["UG"]["PMIN"])
        Aineq = vstack([Aineq, Aineq_temp])
        # 5) PESS_DC - PESS_C + RESS <= PESS_DC_MAX
        Aineq_temp = zeros((T, nx))
        for i in range(T):
            Aineq_temp[i][i * NX + PESS_DC] = 1
            Aineq_temp[i][i * NX + PESS_C] = -1
            Aineq_temp[i][i * NX + RESS] = 1
            bineq.append(model["ESS"]["PMAX_DIS"])
        Aineq = vstack([Aineq, Aineq_temp])
        # 6) PESS_DC - PESS_C - RESS >= -PESS_C_MAX
        Aineq_temp = zeros((T, nx))
        for i in range(T):
            Aineq_temp[i][i * NX + PESS_DC] = -1
            Aineq_temp[i][i * NX + PESS_C] = 1
            Aineq_temp[i][i * NX + RESS] = 1
            bineq.append(model["ESS"]["PMAX_CH"])
        Aineq = vstack([Aineq, Aineq_temp])
        # 7) EESS - RESS*delta >= EESSMIN
        Aineq_temp = zeros((T, nx))
        for i in range(T):
            Aineq_temp[i][i * NX + EESS] = -1
            Aineq_temp[i][i * NX + RESS] = configuration_time_line.default_time["Time_step_ed"] / 3600
            bineq.append(-model["ESS"]["SOC_MIN"] * model["ESS"]["CAP"])
        Aineq = vstack([Aineq, Aineq_temp])
        # 8) EESS + RESS*delta <= EESSMAX
        Aineq_temp = zeros((T, nx))
        for i in range(T):
            Aineq_temp[i][i * NX + EESS] = 1
            Aineq_temp[i][i * NX + RESS] = configuration_time_line.default_time["Time_step_ed"] / 3600
            bineq.append(model["ESS"]["SOC_MAX"] * model["ESS"]["CAP"])
        Aineq = vstack([Aineq, Aineq_temp])
        # 9) RG + RUG + RESS >= sum(Load)*beta + sum(PV)*beta_pv + sum(WP)*beta_wp

        # No reserve requirement
        # 10) PUG-PUG_positive<=PUG_SET_POINT
        Aineq_temp = zeros((T, nx))
        for i in range(T):
            Aineq_temp[i][i * NX + PUG] = 1
            Aineq_temp[i][i * NX + PUG_positive] = -1
            bineq.append(model["UG"]["COMMAND_PG"][i])
        # 11) PUG+PUG_negative>=PUG_SET_POINT
        Aineq_temp = zeros((T, nx))
        for i in range(T):
            Aineq_temp[i][i * NX + PUG] = -1
            Aineq_temp[i][i * NX + PUG_negative] = -1
            bineq.append(-model["UG"]["COMMAND_PG"][i])
        # 12) PMG-PMG_positive<=PMG_SET_POINT
        Aineq_temp = zeros((T, nx))
        for i in range(T):
            Aineq_temp[i][i * NX + PMG] = 1
            Aineq_temp[i][i * NX + PMG_positive] = -1
            bineq.append(model["PMG"][i])
        # 13) PMG+PMG_negative>=PMG_SET_POINT
        Aineq_temp = zeros((T, nx))
        for i in range(T):
            Aineq_temp[i][i * NX + PMG] = -1
            Aineq_temp[i][i * NX + PMG_negative] = -1
            bineq.append(-model["PMG"][i])
        # 14) PESS_DC-PESS_C-SOC_positve<=PESS_SET_POINT
        Aineq_temp = zeros((T, nx))
        for i in range(T):
            Aineq_temp[i][i * NX + PESS_DC] = 1
            Aineq_temp[i][i * NX + PESS_C] = -1
            Aineq_temp[i][i * NX + SOC_positive] = -1
            bineq.append(model["ESS"]["COMMAND_PG"][i])
        # 15) PESS_DC-PESS_C+SOC_negative>=PESS_SET_POINT
        Aineq_temp = zeros((T, nx))
        for i in range(T):
            Aineq_temp[i][i * NX + PESS_DC] = -1
            Aineq_temp[i][i * NX + PESS_C] = 1
            Aineq_temp[i][i * NX + SOC_positive] = -1
            bineq.append(-model["ESS"]["COMMAND_PG"][i])

        c = [0] * NX
        if model["DG"]["COST_MODEL"] == 2:
            c[PG] = model["DG"]["COST"][1]
        else:
            c[PG] = model["DG"]["COST"][0]
        c[PUG] = model["UG"]["COST"][0]
        c[PESS_C] = model["ESS"]["COST_CH"][0]
        c[PESS_DC] = model["ESS"]["COST_DIS"][0]
        # The sheding cost
        c[PPV] = -model["PV"]["COST"]
        c[PWP] = -model["WP"]["COST"]
        c[PL_AC] = -model["Load_ac"]["COST"][0]
        c[PL_UAC] = -model["Load_uac"]["COST"][0]
        c[PL_DC] = -model["Load_dc"]["COST"][0]
        c[PL_UDC] = -model["Load_udc"]["COST"][0]
        c[PMG_negative] = default_eps["Penalty_ed"]
        c[PMG_positive] = default_eps["Penalty_ed"]
        c[PUG_positive] = default_eps["Penalty_ed"]
        c[PUG_negative] = default_eps["Penalty_ed"]
        c[SOC_positive] = default_eps["Penalty_ed"]
        c[SOC_negative] = default_eps["Penalty_ed"]
        c[PBIC_AC2DC] = default_eps["Penalty_ed"] / 10  # These two items are added to remove the bilinear constraints :1)
        c[PBIC_DC2AC] = default_eps["Penalty_ed"] / 10  # 2)

        C = c * T # The cost parameters
        # Generate the quadratic parameters
        Q = zeros((nx, nx))
        for i in range(T):
            if model["DG"]["COST_MODEL"] == 2:
                Q[i * NX + PG][i * NX + PG] = model["DG"]["COST"][1]
        mathematical_model = {"Q": Q,
                              "c": C,
                              "Aeq": Aeq,
                              "beq": beq,
                              "A": Aineq,
                              "b": bineq,
                              "lb": lb,
                              "ub": ub}

        return mathematical_model

    def problem_formulation_universal(*args):
        # Formulate mathematical models for different operations
        local_model = args[0]
        universal_model = args[1]
        type = args[len(args) - 1]  # The last one is the type
        from configuration import configuration_time_line
        T = configuration_time_line.default_look_ahead_time_step["Look_ahead_time_ed_time_step"]

        ## Formulating the universal energy models
        if type == "Feasible":
            from modelling.power_flow.idx_ed_foramt import PMG, NX
            local_model_mathematical = problem_formulation_tracing.problem_formulation_local(local_model)
            universal_model_mathematical = problem_formulation_tracing.problem_formulation_local(universal_model)
        else:
            from modelling.power_flow.idx_ed_recovery_format import PMG, NX
            local_model_mathematical = problem_formulation_tracing.problem_formulation_local_recovery(local_model)
            universal_model_mathematical = problem_formulation_tracing.problem_formulation_local_recovery(universal_model)
        # Modify the boundary information

        for i in range(T):
            local_model_mathematical["lb"][i * NX + PMG] = -universal_model["LINE"]["STATUS"][i] * \
                                                           universal_model["LINE"]["RATE_A"]
            local_model_mathematical["ub"][i * NX + PMG] = universal_model["LINE"]["STATUS"][i] * \
                                                           universal_model["LINE"]["RATE_A"]
            universal_model_mathematical["lb"][i * NX + PMG] = -universal_model["LINE"]["STATUS"][i] * \
                                                               universal_model["LINE"]["RATE_A"]
            universal_model_mathematical["ub"][i * NX + PMG] = universal_model["LINE"]["STATUS"][i] * \
                                                               universal_model["LINE"]["RATE_A"]
        ## Modify the matrix
        nx = T * NX
        neq = local_model_mathematical["Aeq"].shape[0]  # Number of equality constraint
        nineq = local_model_mathematical["A"].shape[0]  # Number of inequality constraint
        Aeq_compact = zeros((2 * neq, 2 * nx))
        beq_compact = zeros(2 * neq)
        Aineq_compact = zeros((2 * nineq, 2 * nx))
        bineq_compact = zeros(2 * nineq)
        c_compact = zeros(2 * nx)
        # The combination of local ems and universal ems problems
        Aeq_compact[0:neq, 0:nx] = local_model_mathematical["Aeq"]
        Aeq_compact[neq:2 * neq, nx:2 * nx] = universal_model_mathematical["Aeq"]
        beq_compact[0:neq] = local_model_mathematical["beq"]
        beq_compact[neq:2 * neq] = universal_model_mathematical["beq"]

        Aineq_compact[0:nineq, 0:nx] = local_model_mathematical["A"]
        Aineq_compact[nineq:2 * nineq, nx:2 * nx] = universal_model_mathematical["A"]
        bineq_compact[0:nineq] = local_model_mathematical["b"]
        bineq_compact[nineq:2 * nineq] = universal_model_mathematical["b"]

        c_compact[0:nx] = local_model_mathematical["c"]
        c_compact[nx:2 * nx] = universal_model_mathematical["c"]
        c_compact = array(c_compact)

        lb = numpy.append(local_model_mathematical["lb"], universal_model_mathematical["lb"])
        ub = numpy.append(local_model_mathematical["ub"], universal_model_mathematical["ub"])

        Aeq_compact_temp = zeros((T, 2 * nx))
        for i in range(T):
            Aeq_compact_temp[i][i * NX + PMG] = 1
            Aeq_compact_temp[i][nx + i * NX + PMG] = 1
            beq_compact = numpy.append(beq_compact, zeros(1))
        Aeq_compact = vstack([Aeq_compact, Aeq_compact_temp])

        Q_compact = zeros((2 * nx, 2 * nx))
        Q_compact[0:nx, 0:nx] = local_model_mathematical["Q"]
        Q_compact[nx:2 * nx, nx:2 * nx] = universal_model_mathematical["Q"]

        model = {"Q": Q_compact,
                 "c": c_compact,
                 "Aeq": Aeq_compact,
                 "beq": beq_compact,
                 "A": Aineq_compact,
                 "b": bineq_compact,
                 "lb": lb,
                 "ub": ub}

        return model
