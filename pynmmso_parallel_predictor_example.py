from pynmmso import Nmmso
from pynmmso.listeners import ParallelPredictorListener

class My2DProblem:
    @staticmethod
    def fitness(params):
        x = params[0]
        y = params[1]
        return -x**4 + x**3 + 3 * x**2 -y**4 + y**3 + 3 * y**2

    @staticmethod
    def get_bounds():
        return [-2, -2], [3, 3]

def main():
    number_of_fitness_evaluations = 5000

    nmmso = Nmmso(My2DProblem())

    parallel_predictor = ParallelPredictorListener()
    nmmso.add_listener(parallel_predictor)

    nmmso.run(number_of_fitness_evaluations)

    for mode_result in nmmso.get_result():
        print("Mode at {} has value {}".format(mode_result.location, mode_result.value))

    parallel_predictor.print_summary()


if __name__ == "__main__":
    main()