#The transmission line models
#The following models are included:
#1) Transmission lines
import configuration.configuration_default_lines as default_parameters
Line = \
    {
        "TYPE":default_parameters.default_Line["TYPE"],
        "F_BUS":default_parameters.default_Line["F_BUS"],
        "T_BUS":default_parameters.default_Line["T_BUS"],
        "BR_R":default_parameters.default_Line["BR_R"],
        "BR_X":default_parameters.default_Line["BR_X"],
        "BR_B":default_parameters.default_Line["BR_B"],
        "RATE_A":default_parameters.default_Line["RATE_A"],
        "RATE_B":default_parameters.default_Line["RATE_B"],
        "RATE_C":default_parameters.default_Line["RATE_C"],
        "TAP":default_parameters.default_Line["TAP"],
        "SHIFT":default_parameters.default_Line["SHIFT"],
        "STATUS":default_parameters.default_Line["STATUS"],
        "PF":default_parameters.default_Line["PF"],
        "QF":default_parameters.default_Line["QF"],
        "TIME_GENERATED": default_parameters.default_Line["TIME_GENERATED"],
        "TIME_APPLIED": default_parameters.default_Line["TIME_APPLIED"],
        "TIME_COMMANDED": default_parameters.default_Line["TIME_COMMANDED"],
        "COMMAND_STATUS":default_parameters.default_Line["COMMAND_STATUS"],
        "COMMAND_TAP":default_parameters.default_Line["COMMAND_TAP"]
    }

#TYPE, the type of transmission lines, 1: AC lines;2:DC lines;3: AC transformers;4, DC transformers

