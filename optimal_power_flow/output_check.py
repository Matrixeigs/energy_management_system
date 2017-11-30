# Output check procedure for optimal power flow
# The following rules are used to test the feasiblity of output
# 1) Active power balancing of on AC bus
# 2) Reactive power balancing of on DC bus

from copy import deepcopy
from configuration.configuration_time_line import default_look_ahead_time_step
from utils import Logger
logger = Logger("Short_term_dispatch_output_check")
from configuration import configuration_default_generators,configuration_default_load,configuration_convertors,configuration_default_lines

def output_local_check(*args):
    model = args[0] # local ems models

def output_universal_check(*args):
    model = args[0]