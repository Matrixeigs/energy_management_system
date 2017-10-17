## Convertor model in universal energy management system
BUS_I = 0  # integrated mg, multiple convertors supported
CAP = 1  # t, to bus number
EFF_AC2DC = 2  # Efficiency of transferring power from AC to DC
EFF_DC2AC = 3  # Efficiency of transferring power from DC to AC
SMAX = 4  # Apparent power capacity
P_AC2DC = 5  # Active power from AC to DC
P_DC2AC = 6  # Active power from DC to AC
QG = 7  # Active power injected to AC bus

MU_PF = 8  # Kuhn-Tucker multiplier on active power from AC to DC (u/W)
MU_PT = 9  # Kuhn-Tucker multiplier on active power from DC to AC (u/W)
MU_SMAX = 10  # Kuhn-Tucker multiplier for apparent power limitation (u/VA)