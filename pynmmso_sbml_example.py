import roadrunner
import numpy as np
import urllib.request
from pynmmso import Nmmso
from pynmmso.listeners import TraceListener
from pynmmso.wrappers import UniformRangeProblem

class SbmlModelProblem:
    def __init__(self, sbml, experimentData):
        self.sbml = sbml
        self.experimentData = experimentData
        self.rr = None

    def fitness(self, x):
        if self.rr is None:
            self.rr = roadrunner.RoadRunner(self.sbml)

        # Reset road runner for a new simulation
        self.rr.resetToOrigin()

        # Set the parameter values
        self.rr.vs = x[0]
        self.rr.vm = x[1]
        self.rr.Km = x[2]
        self.rr.KI = x[3]
        self.rr.n  = x[4]
        self.rr.ks = x[5]
        self.rr.vd = x[6]
        self.rr.Kd = x[7]
        self.rr.k1 = x[8]
        self.rr.k2 = x[9]

        # Run road runner
        self.rr.timeCourseSelections = ['time', 'M', 'FC', 'FN']
        result = self.rr.simulate(0, 96, 97)

        # Compare simulation result with experiment data for all three
        # species from hour 48 onwards
        sum_of_squares_error = np.sum(np.square(np.array(result[48:, 1:])-self.experimentData))

        # Nmmso finds the maximum so need to negate the sum of squares error
        return -sum_of_squares_error

    def get_bounds(self):
        #  +- 30% of the known original value
        original_values = np.array([1.6, 0.505, 0.5, 1, 4, 0.5, 1.4, 0.13, 0.5, 0.6])
        return 0.7 * original_values, 1.3 * original_values

    def __getstate__(self):
        return {
          'sbml': self.sbml,
          'expData': self.experimentData
        }

    def __setstate__(self, state):
        self.sbml = state['sbml']
        self.experimentData = state['expData']
        # lazy init
        self.rr = None


def main():

    # Obtain SBML model from Biomodels and populate Road Runner
    model = urllib.request.urlopen('http://www.ebi.ac.uk/biomodels-main/download?mid=BIOMD0000000299')
    sbml = model.read().decode('utf-8')
    rr = roadrunner.RoadRunner(sbml)

    # Run the simulation and produce some fake experiment data.  If you have
    # actual experiment data you will not need to run this simulation.
    rr.resetToOrigin()
    rr.timeCourseSelections = ['time', 'M', 'FC', 'FN']
    fake_experiment_data = rr.simulate(0, 96, 97)

    # Reduce the experiment data to be the data from 48 hours
    # onwards when limit cycle has been reached and remove the
    # time from the experiment data
    fake_experiment_data = np.array(fake_experiment_data[48:, 1:])

    # Now run NMMSO to find the modes
    nmmso = Nmmso(UniformRangeProblem(SbmlModelProblem(sbml, fake_experiment_data)), 10)
    nmmso.add_listener(TraceListener(1))
    my_result = nmmso.run(50000)

    for mode_result in my_result:
        print("Mode at {} has value {}".format(mode_result.location, mode_result.value))


if __name__ == "__main__":
    main()
