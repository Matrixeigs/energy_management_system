## The modelling  for generations
# define bus types
AC = 1  # Critical AC generators
UAC = 2  # Non-critical AC generators
DC = 3  # Critical DC generators
UDC = 4  # Critical DC generators

# define the indices
GEN_BUS = 0  # bus number
GEN_TYPE = 1  # type of generators
PG = 2  # Pg, real power output (W)
QG = 3  # Qg, reactive power output (VAr)
RG = 4  # Rg, reserve set point for generators (W, a symmetry up and down reserve is provided.)
QMAX = 5  # Qmax, maximum reactive power output at Pmin (VAr)
QMIN = 6  # Qmin, minimum reactive power output at Pmin (VAr)
SMAX = 7  # Qmin, minimum reactive power output at Pmin (VAr)
VG = 8  # Vg, voltage magnitude setpoint (p.u.)
MBASE = 9  # mBase, total MVA base of this machine, defaults to baseMVA
GEN_STATUS = 10  # status, 1 - machine in service, 0 - machine out of service
PMAX = 11  # Pmax, maximum real power output (MW)
PMIN = 12  # Pmin, minimum real power output (MW)
PC1 = 13  # Pc1, lower real power output of PQ capability curve (MW)
PC2 = 14  # Pc2, upper real power output of PQ capability curve (MW)
QC1MIN = 15  # Qc1min, minimum reactive power output at Pc1 (MVAr)
QC1MAX = 16  # Qc1max, maximum reactive power output at Pc1 (MVAr)
QC2MIN = 17  # Qc2min, minimum reactive power output at Pc2 (MVAr)
QC2MAX = 18  # Qc2max, maximum reactive power output at Pc2 (MVAr)
RAMP_AGC = 19  # ramp rate for load following/AGC (MW/min)
RAMP_10 = 20  # ramp rate for 10 minute reserves (MW)
RAMP_30 = 21  # ramp rate for 30 minute reserves (MW)
RAMP_Q = 22  # ramp rate for reactive power (2 sec timescale) (MVAr/min)
APF = 23  # area participation factor

# included in opf solution, not necessarily in input
# assume objective function has units, u
MU_PMAX = 24  # Kuhn-Tucker multiplier on upper Pg limit (u/MW)
MU_PMIN = 25  # Kuhn-Tucker multiplier on lower Pg limit (u/MW)
MU_QMAX = 26  # Kuhn-Tucker multiplier on upper Qg limit (u/MVAr)
MU_QMIN = 27  # Kuhn-Tucker multiplier on lower Qg limit (u/MVAr)

# Note: When a generator's PQ capability curve is not simply a box and the
# upper Qg limit is binding, the multiplier on this constraint is split into
# it's P and Q components and combined with the appropriate MU_Pxxx and
# MU_Qxxx values. Likewise for the lower Q limits.
