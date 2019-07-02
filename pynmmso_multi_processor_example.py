from pynmmso import Nmmso
from pynmmso import MultiprocessorFitnessCaller

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
    num_workers = 4
    with MultiprocessorFitnessCaller(num_workers) as my_multi_processor_fitness_caller:
        nmmso = Nmmso(MyProblem(), fitness_caller=my_multi_processor_fitness_caller)
        my_result = nmmso.run(number_of_fitness_evaluations)

    for mode_result in my_result:
        print("Mode at {} has value {}".format(mode_result.location, mode_result.value))

if __name__ == "__main__":
    main()