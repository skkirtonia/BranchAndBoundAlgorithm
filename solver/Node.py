from gurobipy import *
import scipy as sp
from solver.Constants import Constants

class BnBNode(Constants):
    def __init__(self, goal, c, A_ub=None, b_ub=None, A_eq=None, b_eq=None, bounds=(0, None), int_var_indicator=[]):

        '''
        the problem is formulated as
        min or max c @ x
        s.t.
        A_ub @ x <= b_ub
        A_eq @ x == b_eq
        lb <= x <= ub

        :param objective: 'max' or 'min'
        :param c: The coefficients of the linear objective function to be minimized.
        :param A_ub: The inequality constraint matrix. Each row of A_ub specifies the coefficients of a linear inequality constraint on x
        :param b_ub: The inequality constraint vector. Each element represents an upper bound on the corresponding value of A_ub @ x.
        :param A_eq: The equality constraint matrix. Each row of A_eq specifies the coefficients of a linear equality constraint on x.
        :param b_eq: The equality constraint vector. Each element of A_eq @ x must equal the corresponding element of b_eq.
        :param bounds: A sequence of (min, max) pairs for each element in x, defining the minimum and maximum values of that decision variable.
                        If a single tuple (min, max) is provided, then min and max will serve as bounds for all decision variables.
                        Use None to indicate that there is no bound. For instance, the default bound (0, None) means
                        that all decision variables are non-negative, and the pair (None, None) means no bounds at all,
                        i.e. all variables are allowed to be any real.

        :param int_var_indicator: A binary array where the 1 indicates the ith variable is an integer variable
        '''

        if int_var_indicator is None:
            int_var_indicator = []
        self.goal = goal
        self.c = c
        self.A_ub = A_ub
        self.b_ub = b_ub
        self.A_eq = A_eq
        self.b_eq = b_eq
        self.bounds = bounds
        self.int_var_indicator = int_var_indicator

        self.all_cuts = [] # tracks all new cuts added to the node
        self.fractional_int_variable_indexes = False # list of fractional variables that need to be integer
        self.solution = None # tracks the incumbent solution
        self.objective = None # tracks the incumbent objective
        self.solve()

    def solve(self):
        res = sp.optimize.linprog(c=self.c, A_ub=self.A_ub, A_eq=self.A_eq, b_ub=self.b_ub, b_eq=self.b_eq,
                                  bounds=self.bounds, method="highs")
        if res.status == 0:
            self.fractional_int_variable_indexes = [i for i, isInt in enumerate(self.int_var_indicator) if
                                                    (int(res.x[i]) != res.x[i] and isInt == 1)]
            if self.goal == self.OBJECTIVE_MINIMIZE:
                self.solution = res.x
                self.objective = res.fun
            elif self.goal == self.OBJECTIVE_MAXIMIZE:
                self.solution = res.x
                self.objective = -res.fun
            else:
                raise "Model sense is not not set to MINIMIZE or MAXIMIZE"
