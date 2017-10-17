# Data format for transmission lines in microgrid park
# define the indices
F_BUS       = 0    # f, from bus number
T_BUS       = 1    # t, to bus number
BR_R        = 2    # r, resistance (p.u.)
BR_X        = 3    # x, reactance (p.u.)
BR_B        = 4    # b, total line charging susceptance (p.u.)
RATE_A      = 5    # rateA, MVA rating A (long term rating)
RATE_B      = 6    # rateB, MVA rating B (short term rating)
RATE_C      = 7    # rateC, MVA rating C (emergency rating)
TAP         = 8    # ratio, transformer off nominal turns ratio
SHIFT       = 9    # angle, transformer phase shift angle (degrees)
BR_STATUS   = 10   # initial branch status, 1 - in service, 0 - out of service
ANGMIN      = 11   # minimum angle difference, angle(Vf) - angle(Vt) (degrees)
ANGMAX      = 12   # maximum angle difference, angle(Vf) - angle(Vt) (degrees)

# included in power flow solution, not necessarily in input
PF          = 13   # real power injected at "from" bus end (W)
QF          = 14   # reactive power injected at "from" bus end (VAr)
PT          = 15   # real power injected at "to" bus end (W)
QT          = 16   # reactive power injected at "to" bus end (VAr)

# included in opf solution, not necessarily in input
# assume objective function has units, u
MU_SF       = 17   # Kuhn-Tucker multiplier on MVA limit at "from" bus (u/VA)
MU_ST       = 18   # Kuhn-Tucker multiplier on MVA limit at "to" bus (u/VA)
MU_ANGMIN   = 19   # Kuhn-Tucker multiplier lower angle difference limit
MU_ANGMAX   = 20   # Kuhn-Tucker multiplier upper angle difference limit
