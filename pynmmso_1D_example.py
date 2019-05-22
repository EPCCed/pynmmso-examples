from pynmmso import Nmmso


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

    nmmso = Nmmso(MyProblem())
    my_result = nmmso.run(number_of_fitness_evaluations)
    for mode_result in my_result:
        print("Mode at {} has value {}".format(mode_result.location, mode_result.value))


if __name__ == "__main__":
    main()