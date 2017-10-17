## Data format for energy storage systems
GEN_BUS = 0  # bus number
TYPE = 1  # 1=Integrated to DC bus;2= integrated to AC bus
PG = 2  # Pg, real power output (W)
QG = 3  # Qg, reactive power output (VAr)
RG = 4  # Rg, reserve set point for generators (W, a symmetry up and down reserve is provided.)
SOC = 5 # State of charge
PMAX = 6  # Pmax, maximum real power output (MW)
PMIN = 7  # Pmin, minimum real power output (MW)
QMAX = 8  # Qmax, maximum reactive power output at Pmin (VAr)
QMIN = 9  # Qmin, minimum reactive power output at Pmin (VAr)
SMAX = 10  # Qmin, minimum reactive power output at Pmin (VAr)
SOCMAX = 11
SOCMIN = 12
CAP = 13
VG = 14  # Vg, voltage magnitude setpoint (p.u.)
MBASE = 15  # mBase, total MVA base of this machine, defaults to baseMVA
STATUS = 16  # status, 1 - machine in service, 0 - machine out of service
APF = 17  # area participation factor

# included in opf solution, not necessarily in input
# assume objective function has units, u
MU_PMAX = 18  # Kuhn-Tucker multiplier on upper Pg limit (u/MW)
MU_PMIN = 19  # Kuhn-Tucker multiplier on lower Pg limit (u/MW)
MU_QMAX = 20  # Kuhn-Tucker multiplier on upper Qg limit (u/MVAr)
MU_QMIN = 21  # Kuhn-Tucker multiplier on lower Qg limit (u/MVAr)
MU_SMAX = 22  # Kuhn-Tucker multiplier on lower Qg limit (u/MVAr)
MU_SOCMAX = 23  # Kuhn-Tucker multiplier on lower Qg limit (u/MVAr)
MU_SOCMIN = 24  # Kuhn-Tucker multiplier on lower Qg limit (u/MVAr)

