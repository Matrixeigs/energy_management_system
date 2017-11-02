## The mixed integer solver for universal energy management system
# Two software packages are used to build the mathmatical models for uems.

from numpy import Inf, ones
from gurobipy import *

def milp_gurobi(c, Aeq=None, beq=None, A=None, b=None, xmin=None, xmax=None, vtypes=None, opt=None):
    """Branch and bound method for mix_integer linear programming (MILP).
        Minimize a linear objective function, subject to optional linear constraints and variable bounds::

                min f(x) := inner(c,x)
                 x

        subject to::

                A*x == beq          (linear constraints, equality)
                A*x <= b            (linear constraints, inequality)
                xmin <= x <= xmax   (variable bounds)
                x {binary, discrete, continuous }

        All parameters are optional except C and vtype.
        @param c: Linear function that evaluates the objective function
        @type f_fcn: array
        @param Aeq: Optional equality linear constraints.
        @type Aeq: csr_matrix
        @param beq: Optional equality linear constraints.
        @type beq: array
        @param A: Optional linear constraints.
        @type A: csr_matrix
        @param b: Optional linear constraints. Default values are M{Inf}.
        @type b: array
        @param xmin: Optional lower bounds on the M{x} variables, defaults are
                     M{-Inf}.
        @type xmin: array
        @param xmax: Optional upper bounds on the M{x} variables, defaults are
                     M{Inf}.
        @type xmax: array
        @param vtype: list to depict the variable types, i.e.binary, discrete, continuous.
        @type vtypr: list
        @param opt: optional options dictionary with the following keys, all of
                    which are also optional (default values shown in parentheses)
        @type opt: dict

        @rtype: dict
        @return: The solution dictionary has the following keys:
                   - C{x} - solution vector
                   - C{f} - final objective function value
                   - C{converged} - exit status
                       - True = first order optimality conditions satisfied
                       - False = maximum number of iterations reached
                       - None = numerically failed
                   - C{output} - output dictionary with keys:
                       - C{iterations} - number of iterations performed
                       - C{hist} - list of arrays with trajectories of the
                         following: feascond, gradcond, compcond, costcond, gamma,
                         stepsize, obj, alphap, alphad
                       - C{message} - exit message
        """
    nx = c.shape[0]  # number of decision variables
    if A != None:
        nineq = A.shape[0]  # number of equality constraints
    else:
        nineq = 0

    if Aeq != None:
        neq = Aeq.shape[0]  # number of inequality constraints
    else:
        neq = 0
    # Fulfilling the missing informations
    if beq is None or len(beq) == 0: beq = -Inf * ones(neq)
    if b is None or len(b) == 0: b = Inf * ones(nineq)
    if xmin is None or len(xmin) == 0: xmin = -Inf * ones(nx)
    if xmax is None or len(xmax) == 0: xmax = Inf * ones(nx)

    # modelling based on the high level gurobi api
    try:
        gurobi_model = Model("MIP")
        # Declear the variables
        x = {}
        for i in range(nx):
            if vtypes[i] == "b" or vtypes[i] == "B":
                x[i] = gurobi_model.addVar(lb=xmin[i], ub=xmax[i], vtype=GRB.BINARY, name='"x{0}"'.format(i))
            elif vtypes[i] == "d" or vtypes[i] == "D":
                x[i] = gurobi_model.addVar(lb=xmin[i], ub=xmax[i], vtype=GRB.INTEGER, name='"x{0}"'.format(i))
            else:
                x[i] = gurobi_model.addVar(lb=xmin[i], ub=xmax[i], vtype=GRB.CONTINUOUS, name='"x{0}"'.format(i))
        # Constraints set
        # Equal constraints
        if neq != 0:
            for i in range(neq):
                expr = 0
                for j in range(nx):
                    expr += x[j] * Aeq[i, j]
                gurobi_model.addConstr(lhs=expr, sense=GRB.EQUAL, rhs=beq[i])

        # Inequal constraints
        if nineq != 0:
            for i in range(nineq):
                expr = 0
                for j in range(nx):
                    expr += x[j] * A[i, j]
                gurobi_model.addConstr(lhs=expr, sense=GRB.LESS_EQUAL, rhs=b[i])
        # Set the objective function
        obj = 0
        for i in range(nx):
            obj += x[i] * c[i]

        gurobi_model.setObjective(obj)

        gurobi_model.Params.OutputFlag = 0
        gurobi_model.Params.LogToConsole = 0
        gurobi_model.Params.DisplayInterval = 1
        gurobi_model.optimize()
        xx = []
        for v in gurobi_model.getVars():
            # print('%s %g' % (v.varName, v.x))
            xx.append(v.x)

        obj = obj.getValue()
        # print('Obj: %g' % obj.getValue())

    except GurobiError as e:
        print('Error code ' + str(e.errno) + ": " + str(e))

    except AttributeError:
        print('Encountered an attribute error')

    return xx, obj


def milp_mosek(c, Aeq=None, beq=None, A=None, b=None, xmin=None, xmax=None, vtypes=None, opt=None):
    import mosek
    from numpy import vstack, array
    nx = c.shape[0]  # number of decision variables
    if A != None:
        nineq = A.shape[0]  # number of equality constraints
    else:
        nineq = 0

    if Aeq != None:
        neq = Aeq.shape[0]  # number of inequality constraints
    else:
        neq = 0
    # Fulfilling the missing informations
    if beq is None or len(beq) == 0: beq = -Inf * ones(neq)
    if b is None or len(b) == 0: b = Inf * ones(nineq)
    if xmin is None or len(xmin) == 0: xmin = -Inf * ones(nx)
    if xmax is None or len(xmax) == 0: xmax = Inf * ones(nx)

    # Make a MOSEK environment
    with mosek.Env() as env:
        # Create a task
        with env.Task(0, 0) as task:
            bkc = []
            blc = []
            buc = []
            for i in range(neq):
                bkc.append(mosek.boundkey.ra)
                blc.append(beq[i])
                buc.append(beq[i])

            for i in range(nineq):
                bkc.append(mosek.boundkey.up)
                blc.append(-Inf)
                buc.append(b[i])

            bkx = []
            blx = []
            bux = []
            for i in range(nx):
                bkx.append(mosek.boundkey.ra)
                blx.append(xmin[i])
                bux.append(xmax[i])
            if Aeq != None and A != None:
                A = vstack([Aeq, A], "csr")
            elif Aeq != None and A == None:
                A = Aeq
            # Generate the sparse matrix
            numcon = neq + nineq
            asub = []
            aval = []
            if numcon != 0:
                for i in range(nx):
                    index = []
                    val = []
                    for j in range(numcon):
                        if A[j, i] != 0:
                            index.append(j)
                            val.append(A[j, i])

                    asub.append(index)
                    aval.append(val)
            # Append 'numcon' empty constraints.
            # The constraints will initially have no bounds.
            task.appendcons(numcon)

            # Append 'numvar' variables.
            # The variables will initially be fixed at zero (x=0).
            task.appendvars(nx)

            for j in range(nx):
                # Set the linear term c_j in the objective.
                task.putcj(j, c[j])
                # Set the bounds on variable j
                # blx[j] <= x_j <= bux[j]
                # Input column j of A
                task.putacol(j,  # Variable (column) index.
                             #  Row index of non-zeros in column j.
                             asub[j],
                             aval[j])  # Non-zero Values of column j.
                if vtypes[j] == "b" or vtypes[j] == "B":
                    task.putvartypelist([j], [mosek.variabletype.type_int])
                    task.putvarbound(j, mosek.boundkey.ra, 0, 1)
                elif vtypes[j] == "c" or vtypes[j] == "C":
                    task.putvartypelist([j], [mosek.variabletype.type_int])
                    task.putvarbound(j, bkx[j], blx[j], bux[j])
                else:
                    task.putvartypelist([j], [mosek.variabletype.type_cont])
                    task.putvarbound(j, bkx[j], blx[j], bux[j])

            task.putconboundlist(range(numcon), bkc, blc, buc)

            # Input the objective sense (minimize/maximize)
            task.putobjsense(mosek.objsense.minimize)

            # Optimize the task
            task.optimize()

            prosta = task.getprosta(mosek.soltype.itg)
            solsta = task.getsolsta(mosek.soltype.itg)

            # Output a solution
            xx = [0.] * nx
            task.getxx(mosek.soltype.itg, xx)

            if solsta in [mosek.solsta.integer_optimal, mosek.solsta.near_integer_optimal]:
                print("Optimal solution: %s" % xx)
            elif solsta == mosek.solsta.dual_infeas_cer:
                print("Primal or dual infeasibility.\n")
            elif solsta == mosek.solsta.prim_infeas_cer:
                print("Primal or dual infeasibility.\n")
            elif solsta == mosek.solsta.near_dual_infeas_cer:
                print("Primal or dual infeasibility.\n")
            elif solsta == mosek.solsta.near_prim_infeas_cer:
                print("Primal or dual infeasibility.\n")
            elif mosek.solsta.unknown:
                if prosta == mosek.prosta.prim_infeas_or_unbounded:
                    print("Problem status Infeasible or unbounded.\n")
                elif prosta == mosek.prosta.prim_infeas:
                    print("Problem status Infeasible.\n")
                elif prosta == mosek.prosta.unkown:
                    print("Problem status unkown.\n")
                else:
                    print("Other problem status.\n")
            else:
                print("Other solution status")
        return xx, solsta


##Mixed integer quedratic programming solver
def miqp_gurobi(c, Q, Aeq=None, beq=None, A=None, b=None, xmin=None, xmax=None, vtypes=None, opt=None):
    """Branch and bound method for mix_integer linear programming (MILP).
        Minimize a linear objective function, subject to optional linear constraints and variable bounds::

                min f(x) := inner(c,x) + x'*Q*x/2
                 x

        subject to::

                A*x == beq          (linear constraints, equality)
                A*x <= b            (linear constraints, inequality)
                xmin <= x <= xmax   (variable bounds)
                x {binary, discrete, continuous }

        All parameters are optional except C and vtype.
        @param c: Linear function that evaluates the objective function
        @type f_fcn: array
        @param Aeq: Optional equality linear constraints.
        @type Aeq: csr_matrix
        @param beq: Optional equality linear constraints.
        @type beq: array
        @param A: Optional linear constraints.
        @type A: csr_matrix
        @param b: Optional linear constraints. Default values are M{Inf}.
        @type b: array
        @param xmin: Optional lower bounds on the M{x} variables, defaults are
                     M{-Inf}.
        @type xmin: array
        @param xmax: Optional upper bounds on the M{x} variables, defaults are
                     M{Inf}.
        @type xmax: array
        @param vtype: list to depict the variable types, i.e.binary, discrete, continuous.
        @type vtypr: list
        @param opt: optional options dictionary with the following keys, all of
                    which are also optional (default values shown in parentheses)
        @type opt: dict

        @rtype: dict
        @return: The solution dictionary has the following keys:
                   - C{x} - solution vector
                   - C{f} - final objective function value
                   - C{converged} - exit status
                       - True = first order optimality conditions satisfied
                       - False = maximum number of iterations reached
                       - None = numerically failed
                   - C{output} - output dictionary with keys:
                       - C{iterations} - number of iterations performed
                       - C{hist} - list of arrays with trajectories of the
                         following: feascond, gradcond, compcond, costcond, gamma,
                         stepsize, obj, alphap, alphad
                       - C{message} - exit message
        """
    nx = c.shape[0]  # number of decision variables
    if A != None:
        nineq = A.shape[0]  # number of equality constraints
    else:
        nineq = 0

    if Aeq != None:
        neq = Aeq.shape[0]  # number of inequality constraints
    else:
        neq = 0
    # Fulfilling the missing informations
    if beq is None or len(beq) == 0: beq = -Inf * ones(neq)
    if b is None or len(b) == 0: b = Inf * ones(nineq)
    if xmin is None or len(xmin) == 0: xmin = -Inf * ones(nx)
    if xmax is None or len(xmax) == 0: xmax = Inf * ones(nx)

    # modelling based on the high level gurobi api
    try:
        gurobi_model = Model("MIP")
        # Declear the variables
        x = {}
        for i in range(nx):
            if vtypes[i] == "b" or vtypes[i] == "B":
                x[i] = gurobi_model.addVar(lb=xmin[i], ub=xmax[i], vtype=GRB.BINARY, name='"x{0}"'.format(i))
            elif vtypes[i] == "d" or vtypes[i] == "D":
                x[i] = gurobi_model.addVar(lb=xmin[i], ub=xmax[i], vtype=GRB.INTEGER, name='"x{0}"'.format(i))
            else:
                x[i] = gurobi_model.addVar(lb=xmin[i], ub=xmax[i], vtype=GRB.CONTINUOUS, name='"x{0}"'.format(i))
        # Constraints set
        # Equal constraints
        if neq != 0:
            for i in range(neq):
                expr = 0
                for j in range(nx):
                    expr += x[j] * Aeq[i, j]
                gurobi_model.addConstr(lhs=expr, sense=GRB.EQUAL, rhs=beq[i])

        # Inequal constraints
        if nineq != 0:
            for i in range(nineq):
                expr = 0
                for j in range(nx):
                    expr += x[j] * A[i, j]
                gurobi_model.addConstr(lhs=expr, sense=GRB.LESS_EQUAL, rhs=b[i])
        # Set the objective function
        obj = 0
        for i in range(nx):
            obj += x[i] * c[i]

        # Add the quadratic items
        for i in range(nx):
            for j in range(nx):
                obj += x[i] * x[j] * Q[i][j]/2

        gurobi_model.setObjective(obj)

        gurobi_model.Params.OutputFlag = 0
        gurobi_model.Params.LogToConsole = 0
        gurobi_model.Params.DisplayInterval = 1
        gurobi_model.optimize()
        xx = []
        for v in gurobi_model.getVars():
            # print('%s %g' % (v.varName, v.x))
            xx.append(v.x)

        obj = obj.getValue()
        # print('Obj: %g' % obj.getValue())

    except GurobiError as e:
        print('Error code ' + str(e.errno) + ": " + str(e))

    except AttributeError:
        print('Encountered an attribute error')

    return xx, obj


if __name__ == "__main__":
    # A test problem from Gurobi
    #  maximize
    #        x +   y + 2 z
    #  subject to
    #        x + 2 y + 3 z <= 4
    #        x +   y       >= 1
    #  x, y, z binary

    from numpy import array
    from scipy.sparse import csr_matrix

    c = array([1, 1, 2])
    A = csr_matrix(array([[1, 2, 3],
                          [-1, -1, 0]]))  # A sparse matrix
    b = array([4, -1])
    vtypes = []
    vtypes.append('b')
    vtypes.append('b')
    vtypes.append('b')

    solution_gurobi = milp_gurobi(c, A=A, b=b, vtypes=vtypes)

    solution_mosek = milp_mosek(c, A=A, b=b, vtypes=vtypes)

    # print(solution_gurobi)
    # print(solution_mosek)
