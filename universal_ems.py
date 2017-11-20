## Main entrance for the universal energy management (UEMS).
# Documentation for the UMES.
# \author: Tianyang Zhao.
# \date: 20 November 2017

# The following packages are required to deploy UEMS
# 1) Python 3.6+
# 2) MySQL
# 3) Zeromq
# 4) APScheduler
# 5) Gurobi*(commercial use only)
# 6) Mosek*(Commercial use only)

from apscheduler.schedulers.blocking import BlockingScheduler  # Scheduler is based on APS

import configuration.configuration_database as db_configuration  # The settings of databases


from sqlalchemy import create_engine  # Import the database toolbox
from sqlalchemy.orm import sessionmaker

from utils import Logger

import modelling.information_exchange_pb2 as opf_model # The information model of optimal power flow
import modelling.dynamic_operation_pb2 as economic_dispatch_info # The information model of economic dispatch
import zmq # The information channel

from unit_commitment.main import long_term_operation # long term operation
from economic_dispatch.main import middle_term_operation # middle term operation
from optimal_power_flow.main import short_term_operation # short term operation

class Main():
    ## The main process of UEMS
    # Further functions can be integrated into the functions
    def __init__(self, socket):
        # Implement the start-up test for universal energy management system
        import start_up.start_up_uems
        self.socket = socket
        (self.local_models, self.universal_models, self.operation_mode) = start_up.start_up_uems.start_up_ems.start_up(self.socket)


def run():
    ## Operation process for UEMS
    logger = Logger('Universal_ems_main') # The logger system has been started
    db_str = db_configuration.universal_database["db_str"] # Database format
    engine = create_engine(db_str, echo=False) # Create engine for universal energy management system databases
    Session = sessionmaker(bind=engine) # Create engine for target database
    session_uems = Session() # Create session for universal energy management system
    # IP = "10.25.196.56"
    IP = "*"
    # Start the information connection
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind("tcp://" + IP + ":5555")

    socket_upload = context.socket(zmq.REP)  # Upload information channel for local EMS
    socket_upload.bind("tcp://" + IP + ":5556")

    socket_download = context.socket(zmq.REQ)  # Download information channel for local EMS
    socket_download.bind("tcp://" + IP + ":5557")

    initialize = Main(socket)
    universal_models = initialize.universal_models
    local_models = initialize.local_models
    # Start the input information
    info_ed = economic_dispatch_info.local_sources() # Dynamic information for economic dispatch
    info_uc = economic_dispatch_info.local_sources() # Dynamic information for unit commitment
    info_opf = opf_model.informaiton_exchange() # Optimal power flow modelling

    # Generate different processes
    logger.info("The short term process in UEMS starts!")
    sched_short_term = BlockingScheduler()  # The schedulor for the optimal power flow
    sched_short_term.add_job(short_term_operation.short_term_operation_uems, 'cron',
                             args=(universal_models, local_models, socket_upload, socket_download, info_opf,
                                   session_uems), minute='0-59',
                             second='1')  # The operation is triggered minutely, this process will start at **:01
    sched_short_term.start()

    logger.info("The middle term process in UEMS starts!")
    sched_middle_term = BlockingScheduler()  # The schedulor for the optimal power flow
    sched_middle_term.add_job(middle_term_operation.middle_term_operation_uems, 'cron',
                             args=(universal_models, local_models, socket_upload, socket_download, info_ed,
                                   session_uems), minute='*/5',
                             second='1')  # The operation is triggered every 5 minute
    sched_middle_term.start()

    short_term_operation.short_term_operation_uems(universal_models, local_models, socket_upload, socket_download, info_opf,
            session_uems)

    logger.info("The long term process in UEMS starts!")
    sched_long_term = BlockingScheduler()  # The schedulor for the optimal power flow
    sched_long_term.add_job(long_term_operation.long_term_operation_uems, 'cron',
                              args=(universal_models, local_models, socket_upload, socket_download, info_uc,
                                    session_uems), minute='*/30',
                              second='1')  # The operation is triggered every half an hour
    sched_long_term.start()

if __name__ == "__main__":
    ## Start the main process of universal energy management
    run()
