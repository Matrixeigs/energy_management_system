## Local ems economic dispatch computing format
# Diesel generator set
PG = 0
RG = 1
# Utility grid set
PUG = 2
RUG = 3
# Bi-directional convertor set
PBIC_AC2DC = 4
PBIC_DC2AC = 5
# Energy storage system set
PESS_C = 6
PESS_DC = 7
RESS = 8
EESS = 9
# Neighboring MG set
PMG = 10
# Set points tracing, three dimensions: Utility grid, energy sharing MGs and SOC of ESSs
PUG_positive = 11
PUG_negative = 12
PMG_positive = 13
PMG_negative = 14
SOC_positive = 15
SOC_negative = 16
# Total number of decision variables
NX = 17