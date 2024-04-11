from solver.Constants import Constants
def get_example_problem_1():
    # example branch and bound from Hiller
    c =[4, -2, 7, -1]
    A_ub = [
        [1, 0, 5, 0],
        [1, 1, -1, 0],
        [6, -5, 0, 0],
        [-1, 0, 2, -2]
    ]
    A_eb = None
    b_ub = [10, 1, 0, 3]
    b_eb = None
    bounds = (0, None)
    int_var_indicator = [1, 1, 1, 0]

    objective = Constants.OBJECTIVE_MAXIMIZE
    return c, A_ub, A_eb, b_ub, b_eb, bounds, int_var_indicator, objective


def get_example_problem_2():
    # example branch and bound from Hiller
    c =[3, 1, 2]
    A_ub = [
        [-3, -6, -5]
    ]
    A_eb = None
    b_ub = [-9]
    b_eb = None
    bounds = (0, 1)
    int_var_indicator = [1, 1, 1]

    objective = Constants.OBJECTIVE_MINIMIZE
    return c, A_ub, A_eb, b_ub, b_eb, bounds, int_var_indicator, objective
