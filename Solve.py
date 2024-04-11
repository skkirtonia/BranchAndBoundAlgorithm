import DataMIP
from solver.Constants import Constants
from solver.BnB import BnB


c, A_ub, A_eb, b_ub, b_eb, bounds, int_var_indicator, objective = DataMIP.get_example_problem_2()

BnB = BnB(objective= objective, c=c, A_ub=A_ub, b_ub=b_ub, A_eq=A_eb, b_eq=b_eb,
          bounds=bounds, int_var_indicator=int_var_indicator,
          verbose=False, node_selection_rule=Constants.DEPTH_FIRST_NODE_SELECTION,
          variable_selection_rule=Constants.VARIABLE_SELECTION_LEAST_FRACTIONAL)

print("Incumbent Objective = ", BnB.incumbent_objective)
print("Incumbent Solution = ", BnB.incumbent_solution)
print("Node explored = ", BnB.counter_node_solved)
