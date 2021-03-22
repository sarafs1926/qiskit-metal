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
from qiskit_metal.renderers.renderer_ansys.hfss_renderer import QHFSSRenderer

# w_p is values at poles
def calc_effective_impedence_for_port(yindex : str, hfss: QHFSSRenderer):
    """
    Equation found in:
    Black-box superconducting circuit quantization Simon E. Nigg, Hanhee Paik, Brian Vlastakis, Gerhard Kirchmair, Shyam Shankar,
    Luigi Frunzio, Michel Devoret, Robert Schoelkopf and Steven Girvin
    https://arxiv.org/pdf/1204.0587.pdf Page 3,
    Equation 4, (right hand side equation for Effective Impedence (Z^eff_p)

    This function only calculated the effective impedance (for all frequencies) between to ports (ports 'a' and 'b' of Yab in the given string)
    Args:

    """
    freqs, Pcurves, _ = hfss.get_params(yindex) #PCurves is Yab for given freqs

    # get gradient

    # find where Img(Y) is - to _ (or 0)

    # calculate weighted slopes

    # return slopes


    #imaginary_grad =  np.gradient(port_admittance_matrix, axis=axis).imag * 1j #clarifying for mulitiplication that .imag is imaginary

   # return 2/(port_admittance_matrix * imaginary_grad)



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
