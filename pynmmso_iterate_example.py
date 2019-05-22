from pynmmso import Nmmso


class MyProblem:
    @staticmethod
    def fitness(params):
        x = params[0]
        return -x**4 + x**3 + 3 * x**2

    @staticmethod
    def get_bounds():
        return [-2], [2]


def main():
    number_of_fitness_evaluations = 1000

    nmmso = Nmmso(MyProblem())

    while nmmso.evaluations < number_of_fitness_evaluations:
        nmmso.iterate()
        for swarm in nmmso.swarms:
            print("Swarm {} has {} particles.".format(swarm.id, swarm.number_of_particles))

    for mode_result in nmmso.get_result():
        print("Mode at {} has value {}".format(mode_result.location, mode_result.value))


if __name__ == "__main__":
    main()