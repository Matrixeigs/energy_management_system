## Main entrance for the universal energy management (UEMS).
# Documentation for the UMES.
# \author: Tianyang Zhao.
# \date:
# The following packages are required to deploy UEMS
# 1) Python 3.6+
# 2) MySQL
# 3) Zeromq
# 4) APScheduler
# 5) Gurobi*(commercial use only)
# 6) Mosek*(Commercial use only)

from apscheduler.schedulers.blocking import BlockingScheduler  # Time scheduler
import configuration.configuration_database as db_configuration  # The settings of databases
from sqlalchemy import create_engine  # Import the database toolbox
from sqlalchemy.orm import sessionmaker
from utils import Logger



class Main():
    ## The main process of UEMS
    # Further functions can be integrated into the functions
    def __init__(self, socket):
        # Implement the start-up test for universal energy management system
        import start_up.start_up_uems
        self.socket = socket
        (self.local_models, self.universal_models, self.operation_mode) = start_up.start_up_uems.start_up_ems.start_up(
            self.socket)


def run():
    ## Operation process for UEMS
    ## Import package for information and communication
    import zmq
    ## Import information model
    import modelling.information_exchange_pb2 as info_exchange
    import optimal_power_flow.main
    import economic_dispatch.main
    logger = Logger('Universal_ems_main')
    db_str = db_configuration.universal_database["db_str"]
    engine = create_engine(db_str, echo=False)
    Session = sessionmaker(bind=engine)
    session_short_term_operation = Session()
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
    info = info_exchange.informaiton_exchange()

    # Generate different processes
    # logger.info("The optimal power flow process in UEMS starts!")
    # sched_short_term = BlockingScheduler()  # The schedulor for the optimal power flow
    # sched_short_term.add_job(optimal_power_flow.main.short_term_operation.short_term_operation_uems, 'cron',
    #                          args=(universal_models, local_models, socket_upload, socket_download, info,
    #                                session_short_term_operation), minute='0-59',
    #                          second='1')  # The operation is triggered minutely
    # sched_short_term.start()
    sched_middle_term = BlockingScheduler()  # The schedulor for the optimal power flow
    sched_middle_term.add_job(economic_dispatch.main.middle_term_operation.middle_term_operation_uems, 'cron',
                             args=(universal_models, local_models, socket_upload, socket_download, info,
                                   session_short_term_operation), minute='0-59',
                             second='／10')  # The operation is triggered minutely
    sched_middle_term.start()

if __name__ == "__main__":
    ## universal ems database
    run()
