from pynmmso import Nmmso
from pynmmso.wrappers import UniformRangeProblem

class MyProblem:
    @staticmethod
    def fitness(params):
        x = params[0]
        return -x**4 + x**3 + 3 * x**2

    @staticmethod
    def get_bounds():
        return [-2], [3]


def main():
    number_of_fitness_evaluations = 1000
    problem = UniformRangeProblem(MyProblem())
    nmmso = Nmmso(problem)
    my_result = nmmso.run(number_of_fitness_evaluations)
    for mode_result in my_result:
        print("Mode at {} has value {}".format(mode_result.location, mode_result.value))

    # The internals of the Nmmso object will be in the uniform parameter space
    for swarm in nmmso.swarms:
        print("Swarm id: {} uniform parameter space location : {}  original parameter space location: {}".format(
            swarm.id, swarm.mode_location, problem.remap_parameters(swarm.mode_location)))


if __name__ == "__main__":
    main()