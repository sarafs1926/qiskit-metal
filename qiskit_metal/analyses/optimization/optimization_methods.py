"""This code contains basic methods of optimization.

Key References:
    TODO

"""

from numpy import asarray, sqrt, argmin

def derivative(objective, r, desired_value, delta):

    """Numerical differentiation using finite differences.

            Args:
                objective (function): The black-box function used in optimization.
                r (array): Vector corresponding to the current black-box function solution
                desired_value (float): The desired value from black-box function.
                delta (float): Difference for numerical derivative.


            Returns:
                * gradient (array): The approximate gradient around r.
            Tuple contents:

            """

    delta = asarray([delta] + [0 for _ in range(len(r) - 1)])
    gradient = []

    while len(gradient) < len(r):
        fprime = (objective(r + delta, desired_value, "abs")-objective(r-delta, desired_value, "abs"))/(2*sum(delta))
        gradient += [fprime]
        delta[:] = asarray(list(delta[len(delta) - 1:len(delta)]) + list(delta[0:len(delta) - 1]))

    return asarray(gradient)


def adadelta_gradient_descent_optimization(initial_conditions, desired_value, bounds, objective, derivative=derivative,
                                           display="none", num_inter=1000, delta=1e-10, rho=0.99, epsilon=1e-5,
                                           valued_percentage="5%"):

    """Gradient descent optimization method based off of the Adadelta algorithm.

        Args:
            initial_conditions (list/numpy array): The starting point of the descent (initial conditions).
            desired_value (float): The desired value from black-box function.
            bounds (list): Spatial limits of optimization.
            objective (function): The black-box function used in optimization.
            derivative (function): The derivative of the objective function
                Defaults to numerical differentiation using finite differences.
            display (str): Output type during optimization.
                Defaults to "none"
            num_inter (int): Number of iterations.
                Defaults to 1000
            delta (float): Difference for numerical derivative.
                Defaults to 1e-10
            rho (float): Hyperparameter that acts as a momentum for the partial derivatives. (~ 0.9)
                Defaults to 0.99
            epsilon (float): Hyperparameter that is added to avoid a divide by zero error and to help propel the
             algorithm
            when the decaying moving average squared change and decaying moving average squared gradient are zero (1e-3
            or 1e-8)
                Defaults to 1e-5
            valued_percentage (str): Acceptable percentage error from desired value
                Defaults to "5%"

        Returns:
            tuple: Contents outlined below

        Tuple contents:

            * solutions (array): Array of possible solutions searched during descent.
            * solution_evaluations (array): Array of black-box function values returned during descent.
            * solution (array): Array of values to the best solution to the descent optimized toward the desired value.
            * solution_evaluation (float): Black-box function value determined from the solution.
            * solution_evaluation (float): Percent error between Black-box function value and desired value.

        """

    initial_conditions = asarray(initial_conditions)
    bounds = asarray(bounds)

    def percent_error(actual, theoretical):
        return abs((actual - theoretical) / theoretical)

    def end(solutions, solution_evaluations):

        solution_abs = abs(solution_evaluations - desired_value)
        i_min = argmin(solution_abs)
        del solution_abs
        percentage_error = percent_error(solution_evaluations[i_min], desired_value) * 100

        print('\n>Solution: f(%s) = %.5f; Percentage from desired value = %.5f' % (solutions[i_min],
                                                                                round(solution_evaluations[i_min], 5),
                                                                                round(percentage_error, 5)
                                                                                ))

        return tuple([solutions, solution_evaluations, solutions[i_min], solution_evaluations[i_min], percentage_error])

    valued_percentage = float(valued_percentage.strip("%")) / 100.0
    solutions, solution, solution_evaluations, percentage_away = list(), initial_conditions, list(), None

    square_gradient_avg = [0.0 for _ in range(bounds.shape[0])]
    square_parameter_avg = [0.0 for _ in range(bounds.shape[0])]

    for iteration in range(num_inter):

        gradient = derivative(objective, solution, desired_value, delta)

        for i in range(gradient.shape[0]):
            square_gradient_avg[i] = (square_gradient_avg[i] * rho) + ((gradient[i] ** 2.0) * (1.0 - rho))

        new_solution = list()

        for i in range(solution.shape[0]):
            alpha = (epsilon + sqrt(square_parameter_avg[i])) / (epsilon + sqrt(square_gradient_avg[i]))
            change = alpha * gradient[i]
            square_parameter_avg[i] = (square_parameter_avg[i] * rho) + (change ** 2.0 * (1.0 - rho))
            new_solution.append(solution[i] - change)

        solution = asarray(new_solution)
        solution_evaluation = objective(solution, desired_value, "true")
        solutions.append(solution)
        solution_evaluations.append(solution_evaluation)
        percentage_away = percent_error(solution_evaluation, desired_value)

        for bound in range(len(bounds)):
            if solution[bound] > bounds[bound][1] or solution[bound] < bounds[bound][0]:
                print("Bound Reached")
                return end(asarray(solutions), asarray(solution_evaluations))

        if display == "iteration":
            print(f'>#{iteration + 1} f({solution}) = {round(solution_evaluation, 5)}; Percentage from desired value = {round(percentage_away, 5)}')
        elif display == "percentage completed":

            print(f">{str(round((iteration + 1)/num_inter*100.0, 5))+'%'} f({solution}) = {round(solution_evaluation, 5)}; Percentage from desired value = {round(percentage_away, 5)}")
        elif display == "both":
            print(f">{iteration+1}, {str(round((iteration + 1)/num_inter*100.0, 5))+'%'} f({solution}) = {round(solution_evaluation, 5)}; Percentage from desired value = {round(percentage_away, 5)}")
        elif display == "none":
            pass

        if percentage_away <= valued_percentage:
            return end(asarray(solutions), asarray(solution_evaluations))

    return end(asarray(solutions), asarray(solution_evaluations))
