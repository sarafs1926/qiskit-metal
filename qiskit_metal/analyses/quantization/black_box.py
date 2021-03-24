# -*- coding: utf-8 -*-

# This code is part of Qiskit.
#
# (C) Copyright IBM 2017, 2021.
#
# This code is licensed under the Apache License, Version 2.0. You may
# obtain a copy of this license in the LICENSE.txt file in the root directory
# of this source tree or at http://www.apache.org/licenses/LICENSE-2.0.
#
# Any modifications or derivative works of this code must retain this
# copyright notice, and modified files need to carry a notice indicating
# that they have been altered from the originals.
"""
Black Box Quantization
"""


# rows how many frequency points we take in
import numpy as np
import math
from qiskit_metal.renderers.renderer_ansys.hfss_renderer import QHFSSRenderer


class CalculateEffectiveImpedanceOnPorts:
    FREQ = 0
    PCURV = 1
    GRAD = 2

    @classmethod
    def calculate_effective_impedance_on_ports(self, freqs, pcurves):
        """
        Equation found in:
        Black-box superconducting circuit quantization Simon E. Nigg, Hanhee Paik, Brian Vlastakis, Gerhard Kirchmair, Shyam Shankar,
        Luigi Frunzio, Michel Devoret, Robert Schoelkopf and Steven Girvin
        https://arxiv.org/pdf/1204.0587.pdf Page 3,
        Equation 4, (right hand side equation for Effective Impedence (Z^eff_p)
        Get input from hfss.get_params()

        This function only calculated the effective impedance (for all frequencies) between to ports (ports 'a' and 'b' of Yab in the given string)
        Args:

        """
        # get gradient
        grad = np.gradient(pcurves)
        info = zip(freqs, pcurves, grad)

        # find where Img(Y) is - to + (or 0)
        past = (0, 0, 0)
        intercepts = []
        for i in info:
            if i[self.PCURV].imag == 0:
                intercepts.append(i)
            elif past[self.PCURV].imag * i[self.PCURV].imag < 0:
                intercepts.append(self.calculated_weighted_intercept_slope(past, i))
            past = i

        intercepts = np.array(intercepts)
        grad = intercepts[:,self.GRAD]
        freqs = intercepts[:,self.FREQ]
        Z_eff_p = 2/(freqs * grad.imag)

        return Z_eff_p, intercepts


    @classmethod
    def calculated_weighted_intercept_slope(self, prev, post):

        # Turning imaginary part into another "real" axis to find the intersection
        prev_point = np.array([prev[self.FREQ]] + [prev[self.PCURV].real] + [prev[self.PCURV].imag])
        post_point = np.array([post[self.FREQ]] + [post[self.PCURV].real] + [post[self.PCURV].imag])
        # math.dist
        direction_vector = post_point - prev_point

        REAL = 1
        IMAG = 2
        # find intersection at imag
        freq_val_at_imag_intercept = (-1) * (
                    (post_point[IMAG] * direction_vector[self.FREQ] / direction_vector[IMAG]) - post_point[self.FREQ])
        real_val_at_imag_intercept = (-1) * (
                    (post_point[IMAG] * direction_vector[REAL] / direction_vector[IMAG]) - post_point[REAL])

        imag_intercept = [freq_val_at_imag_intercept, real_val_at_imag_intercept + 0j]

        prev_dist = self.find_euclidean_distance(prev_point, imag_intercept)
        post_dist = self.find_euclidean_distance(post_point, imag_intercept)

        prev_dist_scaled = prev_dist / (prev_dist + post_dist)
        post_dist_scaled = post_dist / (prev_dist + post_dist)

        # closer weighs more so swap
        intercept_grad = (prev_dist_scaled * post[self.GRAD]) + post_dist_scaled * prev[self.GRAD]

        return np.array(imag_intercept + [intercept_grad])

    @classmethod
    def find_euclidean_distance(self, prev_point, post_point):
        POST = 1
        PREV = 0
        pairs = zip(prev_point, post_point)
        sum = 0
        for p in pairs:
            sum += (p[POST] - p[PREV]) ** 2

        return sum ** (0.5)

def calc_flux_for_port():
    """
    Equation found in:
    Black-box superconducting circuit quantization Simon E. Nigg, Hanhee Paik, Brian Vlastakis, Gerhard Kirchmair, Shyam Shankar,
    Luigi Frunzio, Michel Devoret, Robert Schoelkopf and Steven Girvin
    https://arxiv.org/pdf/1204.0587.pdf Page 3,
    Equation 4, (left hand side equation for
    Returns:

    """
    pass
