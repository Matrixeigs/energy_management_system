# The main entrance of the optimal power flow in unviersal energy management system
import threading  # Thread management (timeout and return value)
from solvers.mix_integer_solvers import miqp_gurobi,milp_gurobi,milp_mosek  # linear programming solver

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
    Q = args[0]["Q"]
    # Formulate the variable types.
    vtypes = args[0]["vtypes"]


    # (solution,obj,success) = miqp_gurobi(c,Q,Aeq=Aeq, beq=beq,A=A, b=b, xmin=lb,xmax=ub,vtypes=vtypes)
    (solution, obj, success) = milp_gurobi(c, Aeq=Aeq, beq=beq, A=A, b=b, xmin=lb, xmax=ub, vtypes=vtypes)
    # (solution, obj, success) = milp_mosek(c, Aeq=Aeq, beq=beq, A=A, b=b, xmin=lb, xmax=ub, vtypes=vtypes)
    #The return value is the
    res = {"x": solution,
           "obj":obj,
           "success":success>0}

    return res
