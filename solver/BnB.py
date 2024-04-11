import copy
from solver.Node import BnBNode
from solver.Constants import Constants
import heapq


class BnB(Constants):

    def __init__(self, objective, c, A_ub=None, b_ub=None, A_eq=None, b_eq=None, bounds=(0, None), int_var_indicator=[],
                 verbose=False, node_selection_rule=Constants.DEPTH_FIRST_NODE_SELECTION,
                 variable_selection_rule = Constants.VARIABLE_SELECTION_MOST_FRACTIONAL):
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
        :param verbose: True or False to enable verbose output
        :param node_selection_rule: All rules are declared in the Constants class of this project
            DEPTH_FIRST_NODE_SELECTION = 1
            BREADTH_FIRST_NODE_SELECTION = 2
            BEST_FIRST_NODE_SELECTION = 3
        :param variable_selection_rule:  All rules are declared in the Constants class of this project
            VARIABLE_SELECTION_FIRST = 4
            VARIABLE_SELECTION_LAST = 5
            VARIABLE_SELECTION_MOST_FRACTIONAL = 6
            VARIABLE_SELECTION_LEAST_FRACTIONAL = 7
        '''

        self.goal = objective
        self.c = c
        if objective == Constants.OBJECTIVE_MAXIMIZE:
            self.c = [-1*coef for coef in c]
        self.A_ub = A_ub
        self.b_ub = b_ub
        self.A_eq = A_eq
        self.b_eq = b_eq
        self.bounds = bounds
        self.int_var_indicator = int_var_indicator
        self.verbose = verbose
        self.node_selection_rule = node_selection_rule
        self.variable_selection_rule = variable_selection_rule

        self.node_list = []
        self.incumbent_objective = {self.OBJECTIVE_MINIMIZE: float("inf"), self.OBJECTIVE_MAXIMIZE: float("-inf")}[objective]
        self.incumbent_solution = None
        self.counter_node_solved = 1
        self.setup()
        self.start_branching()


    def setup(self):
        if self.node_selection_rule == self.BEST_FIRST_NODE_SELECTION:
            heapq.heapify(self.node_list)

    def get_next_node(self):
        if self.node_selection_rule == self.DEPTH_FIRST_NODE_SELECTION:
            return self.node_list.pop()
        elif self.node_selection_rule == self.BREADTH_FIRST_NODE_SELECTION:
            return self.node_list.pop(0)
        elif self.node_selection_rule == self.BEST_FIRST_NODE_SELECTION:
            obj, node = heapq.heappop(self.node_list)
            return node
        else:
            raise "Node selection rule not found"

    def add_node(self, node, lp_obj=None):
        if self.node_selection_rule == self.DEPTH_FIRST_NODE_SELECTION:
            self.node_list.append(node)
        elif self.node_selection_rule == self.BREADTH_FIRST_NODE_SELECTION:
            self.node_list.append(node)
        elif self.node_selection_rule == self.BEST_FIRST_NODE_SELECTION:
            if self.goal == self.GOAL_MINIMIZE:
                heapq.heappush(self.node_list, (lp_obj, node))
            if self.goal == self.GOAL_MAXIMIZE:
                heapq.heappush(self.node_list, (-1*lp_obj, node))
        else:
            raise "Node selection rule not found"

    def select_next_variable_to_branch(self, node):
        if self.variable_selection_rule == self.VARIABLE_SELECTION_FIRST:
            return node.fractional_int_variable_indexes[0]
        elif self.variable_selection_rule == self.VARIABLE_SELECTION_LAST:
            return node.fractional_int_variable_indexes[-1]
        elif self.variable_selection_rule == self.VARIABLE_SELECTION_MOST_FRACTIONAL:
            most_frac_index = None
            most_frac_value = 0
            for i in node.fractional_int_variable_indexes:
                frac = abs(node.solution[i]-round(node.solution[i]))
                # print(frac)
                if frac>= most_frac_value:
                    most_frac_index = i
                    most_frac_value = frac
            return most_frac_index
        elif self.variable_selection_rule == self.VARIABLE_SELECTION_LEAST_FRACTIONAL:
            least_frac_index = None
            least_frac_value = 0.5
            for i in node.fractional_int_variable_indexes:
                frac = abs(node.solution[i] - round(node.solution[i]))
                # print(frac)
                if frac <= least_frac_value:
                    least_frac_index = i
                    least_frac_value = frac
            return least_frac_index
        else:
            raise "Node selection rule not found"


    def branch_node(self, current_node: BnBNode):
        selected_branching_var_index = self.select_next_variable_to_branch(current_node)
        # Start Branching
        # Construct left node
        A_ub = copy.deepcopy((current_node.A_ub))
        b_ub = copy.deepcopy((current_node.b_ub))
        new_constraint = [0]*len(current_node.c)
        new_constraint[selected_branching_var_index] = 1
        A_ub.append(new_constraint)
        new_constraint_rhs = int(current_node.solution[selected_branching_var_index])
        b_ub.append(new_constraint_rhs)

        new_node_left = BnBNode(
            goal=self.goal,
            c=current_node.c, A_ub=A_ub, b_ub=b_ub,
            A_eq=current_node.A_eq, b_eq=current_node.b_eq,
            bounds=current_node.bounds, int_var_indicator=self.int_var_indicator
        )
        # Keep track of all cuts
        new_node_left.all_cuts = current_node.all_cuts[:]
        new_node_left.all_cuts.append(f"{new_constraint} <= {new_constraint_rhs}")

        # Construct right node
        A_ub = copy.deepcopy((current_node.A_ub))
        b_ub = copy.deepcopy((current_node.b_ub))
        new_constraint = [0] * len(current_node.c)
        new_constraint[selected_branching_var_index] = -1
        A_ub.append(new_constraint)
        new_constraint_rhs = -(int(current_node.solution[selected_branching_var_index])+1)
        b_ub.append(new_constraint_rhs)

        new_node_right = BnBNode(
            goal=self.goal,
            c=current_node.c, A_ub=A_ub, b_ub=b_ub,
            A_eq=current_node.A_eq, b_eq=current_node.b_eq,
            bounds=current_node.bounds, int_var_indicator=self.int_var_indicator
        )
        # Keep track of all cuts
        new_node_right.all_cuts = current_node.all_cuts[:]
        new_node_right.all_cuts.append(f"{new_constraint} <= {new_constraint_rhs}")


        if new_node_right.solution is not None:
            self.add_node(new_node_right, new_node_right.objective)
        else:
            # (1/3) Fathomed due to infeasibility

            self.print_info(new_node_right)
        if new_node_left.solution is not None:
            self.add_node(new_node_left, new_node_left.objective)
        else:
            # (1/3) Fathomed due to infeasibility
            self.print_info(new_node_left)
        self.counter_node_solved += 2

    def fathom_with_integer_solution_and_inferior_solution(self, current_node: BnBNode):
        if self.goal == self.OBJECTIVE_MAXIMIZE:
            if current_node.objective > self.incumbent_objective:
                if current_node.fractional_int_variable_indexes:
                    self.branch_node(current_node)
                else:
                    # (3/3) Fathomed due to finding integer solution
                    self.incumbent_objective = current_node.objective
                    self.incumbent_solution = current_node.solution
            else:
                # print("(2/3) Fathomed due to inferior LP objective than incumbent")
                # (2/3) Fathomed due to inferior LP objective than incumbent
                pass
        elif self.goal == self.OBJECTIVE_MINIMIZE:
            if current_node.objective < self.incumbent_objective:
                if current_node.fractional_int_variable_indexes:
                    self.branch_node(current_node)
                else:
                    # (3/3) Fathomed due to finding integer solution
                    self.incumbent_objective = current_node.objective
                    self.incumbent_solution = current_node.solution
            else:
                # print("(2/3) Fathomed due to inferior LP objective than incumbent")
                # (2/3) Fathomed due to inferior LP objective than incumbent
                pass
        else:
            raise "Model sense is not not set to MINIMIZE or MAXIMIZE"


    def start_branching(self):
        node = BnBNode(
            goal=self.goal,
            c=self.c, A_ub=self.A_ub, b_ub=self.b_ub,
            A_eq=self.A_eq, b_eq=self.b_eq,
            bounds=self.bounds, int_var_indicator=self.int_var_indicator
        )
        self.add_node(node, node.objective)
        print("Starting BnB Tree")
        while self.node_list and self.counter_node_solved<10:
            current_node = self.get_next_node()
            self.print_info(current_node)
            self.fathom_with_integer_solution_and_inferior_solution(current_node)

    def print_info(self, node):
        if self.verbose:
            print("Incumbent", self.incumbent_objective, self.incumbent_solution)
            print("len node list", len(self.node_list))
            print("All Cuts")
            print(node.all_cuts)
            print("Current Solution", node.solution)
            print("Current Objective", node.objective)
            print("fractional_int_variable_indexes", node.fractional_int_variable_indexes)
            print("---------------------------")
