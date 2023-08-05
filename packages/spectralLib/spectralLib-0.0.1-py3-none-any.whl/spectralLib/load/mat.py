# This file is part of spectralLib.
#
# Copyright 2020, Tom George Ampiath, All rights reserved.
#
# spectralLib is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# spectralLib is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with spectralLib.  If not, see <http://www.gnu.org/licenses/>.

import numpy as np
from scipy.io import loadmat


def load_mat_file(file):
    """Returns the spectral datacube from the input MATLAB file

    :param file_name: Path to the .mat file
    :return: spectral datacube or error, if any
    """
    try:
        mat_file = loadmat(file)
    except FileNotFoundError:
        return 0

    var_name = ""

    for key in mat_file:
        value = mat_file[key]
        if isinstance(value, np.ndarray) and len(value.shape) == 3:
            var_name = key
            break

    if var_name == "":
        return 4

    return mat_file[var_name]
