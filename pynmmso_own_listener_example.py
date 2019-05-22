from pynmmso import Nmmso
from pynmmso.listeners import BaseListener


class MyListener(BaseListener):

    def __init__(self):
        self.nmmso = None
        self.iterations = 0

    def set_nmmso(self, nmmso):
        self.nmmso = nmmso

    def iteration_ended(self, n_new_locations, n_mid_evals, n_evol_modes, n_rand_modes, n_hive_samples):
        self.iterations += 1
        print("{},{}".format( self.iterations, len(self.nmmso.swarms)))

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
    nmmso.add_listener(MyListener())
    my_result = nmmso.run(number_of_fitness_evaluations)
    

if __name__ == "__main__":
    main()