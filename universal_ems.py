## Main entrance for the universal energy management (UEMS).
# Documentation for the UMES.
# \author: Tianyang Zhao
# \mail: zhaoty@ntu.edu.sg
# \date: 20 November 2017

# The following packages are required to deploy UEMS
# 1) Python 3.6+
# 2) MySQL
# 3) Zeromq
# 4) APScheduler
# 5) Gurobi*(academic use only)
# 6) Mosek*(academic use only)
# 7）Protocol buffer > 3.4.0. The early version does not have the value attribute

from apscheduler.schedulers.blocking import BlockingScheduler  # Scheduler is based on APS

import configuration.configuration_database as db_configuration  # The settings of databases

from sqlalchemy import create_engine  # Import the database toolbox
from sqlalchemy.orm import sessionmaker

from utils import Logger  # The utility function import from LongQi' work

import modelling.information_exchange_pb2 as opf_model  # The information model of optimal power flow
import modelling.dynamic_operation_pb2 as economic_dispatch_info  # The information model of economic dispatch
import zmq  # The information channel

from unit_commitment.main import long_term_operation  # long term operation
from economic_dispatch.main import middle_term_operation  # middle term operation
from optimal_power_flow.main import short_term_operation  # short term operation


class Main():
    ## The main process of UEMS
    # Further functions can be integrated into the functions
    def __init__(self, socket):
        # Implement the start-up test for universal energy management system
        import start_up.start_up_uems
        self.socket = socket
        try:
            (self.local_model_short, self.local_model_middle, self.local_model_long, self.universal_model_short,
             self.universal_model_middle, self.universal_model_long,
             self.operation_mode) = start_up.start_up_uems.start_up_ems.start_up(self.socket)
        except:
            (self.local_model_short, self.local_model_middle, self.local_model_long,
             self.operation_mode) = start_up.start_up_uems.start_up_ems.start_up(self.socket)


def run():
    ## Operation process for UEMS
    logger = Logger('Universal_ems_main')  # The logger system has been started
    db_str = db_configuration.universal_database["db_str"]  # Database format
    engine = create_engine(db_str, echo=False)  # Create engine for universal energy management system databases
    Session = sessionmaker(bind=engine)  # Create engine for target database

    engine_middle = create_engine(db_str, echo=False)
    Session_middle = sessionmaker(bind=engine_middle)
    session_uems_short = Session()  # Create session for universal energy management system

    session_uems_middle = Session_middle()  # Create session for universal energy management system

    engine_long = create_engine(db_str, echo=False)
    Session_long = sessionmaker(bind=engine_long)
    session_uems_long = Session_long()  # Create session for universal energy management system
    IP = "*"
    # Start the information connection
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind("tcp://" + IP + ":5555")

    socket_upload = context.socket(zmq.REP)  # Upload information channel for local EMS
    socket_upload.bind("tcp://" + IP + ":5556")

    socket_upload_ed = context.socket(zmq.REP)  # Upload information channel for local EMS
    socket_upload_ed.bind("tcp://" + IP + ":5557")

    socket_upload_uc = context.socket(zmq.REP)  # Upload information channel for local EMS
    socket_upload_uc.bind("tcp://" + IP + ":5558")

    socket_download = context.socket(zmq.REQ)  # Download information channel for local EMS
    socket_download.bind("tcp://" + IP + ":5559")

    initialize = Main(socket)  # Initialized the connection between the lems and uems

    local_model_short = initialize.local_model_short
    local_model_middle = initialize.local_model_middle
    local_model_long = initialize.local_model_long

    universal_model_short = initialize.universal_model_short
    universal_model_middle = initialize.universal_model_middle
    universal_model_long = initialize.universal_model_long
    # Start the input information
    info_ed = economic_dispatch_info.local_sources()  # Dynamic information for economic dispatch
    info_uc = economic_dispatch_info.local_sources()  # Dynamic information for unit commitment
    info_opf = opf_model.informaiton_exchange()  # Optimal power flow modelling

    # Generate different processes
    # logger.info("The short term process in UEMS starts!")
    # sched_uems = BlockingScheduler()  # The schedulor for the optimal power flow
    # sched_uems.add_job(short_term_operation.short_term_operation_uems, 'cron',
    #                    args=(universal_model_short, local_model_short, socket_upload, socket_download, info_opf,
    #                          session_uems_short), minute='0-59',
    #                    second='1')  # The operation is triggered minutely, this process will start at **:01
    #
    # logger.info("The middle term process in UEMS starts!")
    # sched_uems.add_job(middle_term_operation.middle_term_operation_uems, 'cron',
    #                    args=(universal_model_middle, local_model_middle, socket_upload_ed, socket_download, info_ed,
    #                          session_uems_middle), minute='*/5',
    #                    second='5')  # The operation is triggered every 5 minute
    #
    # logger.info("The long term process in UEMS starts!")
    # sched_uems.add_job(long_term_operation.long_term_operation_uems, 'cron',
    #                    args=(universal_model_long, local_model_long, socket_upload_uc, socket_download, info_uc,
    #                          session_uems_long), minute='*/30',
    #                    second='30')  # The operation is triggered every half an hour
    # sched_uems.start()
    for i in range(100):
        short_term_operation.short_term_operation_uems(universal_model_short, local_model_short, socket_upload, socket_download, info_opf,
            session_uems_short)
    # middle_term_operation.middle_term_operation_uems(universal_model_middle, local_model_middle, socket_upload_ed,
    #                                                 socket_download, info_ed,session_uems_middle)
    # long_term_operation.long_term_operation_uems(universal_model_long, local_model_long, socket_upload_uc,
    #                                              socket_download, info_uc,
    #                                              session_uems_long)


if __name__ == "__main__":
    ## Start the main process of universal energy management
    run()
