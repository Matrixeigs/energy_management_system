# The main entrance of local energy management system (UEMS)
# Date: 4/Sep/2017
# Authors: Tianyang Zhao
# Mail: zhaoty@ntu.edu.sg
from apscheduler.schedulers.blocking import BlockingScheduler  # Time scheduler

import configuration.configuration_database as db_configuration  # The settings of databases
from sqlalchemy import create_engine  # Import database
from sqlalchemy.orm import sessionmaker
import zmq  # The package for information and communication

import modelling.information_exchange_pb2 as opf_model  # The information model of optimal power flow
import modelling.dynamic_operation_pb2 as economic_dispatch_info  # The information model of economic dispatch

from modelling import generators, loads, energy_storage_systems, convertors
from data_management.information_management import information_receive_send

from start_up import static_information, start_up_lems

from optimal_power_flow.main import short_term_operation
from economic_dispatch.main import middle_term_operation
from unit_commitment.main import long_term_operation

from utils import Logger

logger = Logger("Local_ems")


def run():
    # Define the local models
    (local_model_short, local_model_middle, local_model_long) = start_up_lems.start_up_lems.start_up()
    # Convert local information to sharable information
    static_info = static_information.static_information_generation(local_model_short)
    # Set the database information
    db_str = db_configuration.local_database["db_str"]
    engine = create_engine(db_str, echo=False)
    Session = sessionmaker(bind=engine)
    session_lems_short = Session()
    session_lems_middle = Session()
    session_lems_long = Session()

    # Start the information connection
    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    socket.connect("tcp://localhost:5555")

    socket_upload = context.socket(zmq.REQ)
    socket_upload.connect("tcp://localhost:5556")

    socket_upload_ed = context.socket(zmq.REQ)
    socket_upload_ed.connect("tcp://localhost:5557")

    socket_upload_uc = context.socket(zmq.REQ)
    socket_upload_uc.connect("tcp://localhost:5558")

    socket_download = context.socket(zmq.REP)
    socket_download.connect("tcp://localhost:5559")

    while True:
        socket.send(b"ConnectionRequest")

        message = socket.recv()
        if message == b"Start!":
            logger.info("The connection between the local EMS and universal EMS establishes!")
            break
        else:
            logger.error("Waiting for the connection between the local EMS and universal EMS!")

    information_receive_send.information_send(socket, static_info, 2)

    info_ed = economic_dispatch_info.local_sources()
    info_uc = economic_dispatch_info.local_sources()  # The information model in the
    info_opf = opf_model.informaiton_exchange()  # The optimal power flow modelling
    # By short-term operation process
    logger.info("The short-term process in local ems starts!")
    sched_lems = BlockingScheduler()  # The schedulor for the optimal power flow
    sched_lems.add_job(
        lambda: short_term_operation.short_term_operation_lems(local_model_short, socket_upload, socket_download,
                                                               info_opf,
                                                               session_lems_short),
        'cron', minute='0-59', second='1')  # The operation is triggered minutely

    logger.info("The middle-term process in local EMS starts!")
    sched_lems.add_job(
        lambda: middle_term_operation.middle_term_operation_lems(local_model_middle, socket_upload_ed, socket_download,
                                                                 info_ed,
                                                                 session_lems_middle),
        'cron', minute='*/5', second='5')  # The operation is triggered every five minute

    logger.info("The long term process in local EMS starts!")
    sched_lems.add_job(
        lambda: long_term_operation.long_term_operation_lems(local_model_long, socket_upload_uc, socket_download,
                                                             info_uc,
                                                             session_lems_long),
        'cron', minute='*/30', second='30')  # The operation is triggered every half an hour
    sched_lems.start()
    # for i in range(100):
        # short_term_operation.short_term_operation_lems(local_model_short, socket_upload, socket_download, info_opf,
        #                                        session_lems_short)
        # middle_term_operation.middle_term_operation_lems(local_model_middle, socket_upload_ed, socket_download, info_ed,
        #                                                  session_lems_middle)
        # long_term_operation.long_term_operation_lems(local_model_long, socket_upload_uc, socket_download, info_uc,
        #                                                           session_lems_long)


if __name__ == "__main__":
    ## Start the main process of local energy management system
    run()
