from qiskit_metal.analyses.quantization import black_box
import unittest
import numpy as np



class BlackBoxAnalysis(unittest.TestCase):


    def test_calc_effective_impedence_for_port(self):
        test1 = [ np.array([[[1j,0j],[2j,0j]],[[2j,0j],[4j,0j]],[[3j,0j],[6j,0j]],[[4j,0j],[8j,0j]]]), 0, np.array([
                                                                                                    [[1.,0.],
                                                                                                     [2.,0.]],

                                                                                                    [[1.,0.],
                                                                                                     [2., 0.]],

                                                                                                    [[1., 0.],
                                                                                                     [2., 0.]],

                                                                                                    [[1., 0.],
                                                                                                     [2, 0]]])]
        print (black_box.calc_effective_impedence_for_port(test1[0], test1[1]))
       # assert (test1[2] == black_box.calc_effective_impedence_for_port(test1[0], test1[1])).all()