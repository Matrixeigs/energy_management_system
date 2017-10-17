## Inspired by Pypower and matpower, a self-defined data format for universal energy management system
# define bus types
PQ = 1
PV = 2
REF = 3
NONE = 4

# define the indices
BUS_I = 0  # local ems number (1 to 29997)
BUS_TYPE = 1  # local type
AC_PD = 2  # AC critical real power demand (W)
AC_QD = 3  # AC critical reactive power demand (Var)
UAC_PD = 4  # AC non-critical real power demand (W)
UAC_QD = 5  # AC non-critical reactive power demand (Var)
GS = 6  # Gs, shunt conductance (W at V = 1.0 p.u.)
BS = 7  # Bs, shunt susceptance (VAr at V = 1.0 p.u.)
DC_PD = 8  # DC critical power demand (W)
UDC_PD = 9  # DC non-critical power demand (W)
BUS_AREA = 10  # area number, 1-100
VM = 11  # Vm, voltage magnitude (p.u.)
VA = 12  # Va, voltage angle (degrees)
BASE_KV = 13  # baseKV, base voltage (V)
ZONE = 14  # zone, loss zone (1-999)
VMAX = 15  # maxVm, maximum voltage magnitude (p.u.)
VMIN = 16  # minVm, minimum voltage magnitude (p.u.)
# DC side parameters

# included in opf solution, not necessarily in input
# assume objective function has units, u
LAM_P = 17  # Lagrange multiplier on real power mismatch (u/W)
LAM_Q = 18  # Lagrange multiplier on reactive power mismatch (u/VAr)
MU_VMAX = 19  # Kuhn-Tucker multiplier on upper voltage limit (u/p.u.)
MU_VMIN = 20  # Kuhn-Tucker multiplier on lower voltage limit (u/p.u.)