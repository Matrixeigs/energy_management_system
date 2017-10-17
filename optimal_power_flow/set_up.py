# The main entrance of the optimal power flow in unviersal energy management system
from data_management.information_management import information_receive_send  # The information structure
import optimal_power_flow.problem_formulation as opf_problem_formulation
import threading  # Thread management (timeout and return value)
from scipy import optimize # linear programming solver
import time

class Solving_Thread(threading.Thread):
    # Thread operation with time control and return value
    def __init__(self, parameter):
        threading.Thread.__init__(self)
        self.parameter = parameter
        self.value = 0

    def run(self):
        self.value = solving_procedure(self.parameter)


def solving_procedure(*args):
    # By using linear programming to solve the optimal power flow problem
    # The input is dictionary
    c = args[0]["c"]
    A = args[0]["A"]
    b = args[0]["b"]
    Aeq = args[0]["Aeq"]
    beq = args[0]["beq"]
    lb = args[0]["lb"]
    ub = args[0]["ub"]
    option = {"disp": False}

    # Convert list into tuple
    boundary = tuple()
    for i in range(len(lb)):
        boundary += ((lb[i], ub[i]),)

    res = optimize.linprog(c, A_ub=A, b_ub=b, A_eq=Aeq, b_eq=beq, bounds=boundary, options=option)

    return res


def optimal_power_flow(*args):  # The main entrance
    # The optimal power flow is formulated and the
    # The solution method is based on cvxopt
    # S1: input information check
    # S2: problem formulation
    # S3: problem solving
    # S4: result storage
    # Decouple the models
    socket = args[0]
    opf_info = args[1]
    local_models = args[2]
    universal_models = args[3]

    # Formulate the mathmatical models for computing
    model = opf_problem_formulation.problem_formulaiton(local_models, universal_models)
    # opf_info.dg.extend([dg_info])
    thread = Solving_Thread(model)
    # thread_load_shedding = SolvingThread(random.randint(0, 10))
    thread.daemon = True
    # thread_load_shedding.daemon = True

    thread.start()
    # thread_load_shedding.start()

    thread.join(5)
    # thread_load_shedding.join(5)
    # Assess the solutions
    print("The problem has been solved!")
    #Try to obtain the solution.
    try:
        print(thread.value["x"][13])
    except:
        print("The problem is infeasilbe!")
    # Send set-points back to local EMSs

    opf_info.time_stamp = round(time.time())

    information_receive_send.information_send(socket, opf_info, 2)  # The received information
