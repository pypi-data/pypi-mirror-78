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

from matplotlib import pyplot as plt
from numpy import ndarray

from spectralLib.load.file import load_file


def display_spectral_signature(file, pixel=(0, 0), cli=True, skip_load=False):
    """Function to display spectral signature at given pixel coordinates

    :param file: Input file - file name or data cube
    :param pixel: Pixel coordinates (default (0, 0))
    :param cli: Boolean variable. If set as True, displays the spectral signature in matplotlib
                window. If set as False, returns the signature as a list. The GUI app using
                this library can display the signature using this data. (default True)
    :param skip_load: Boolean variable. If set as True, skips loading the dataset (To improve
                      performance, if data is already loaded). Can be used when calling this
                      function to display spectral signature corresponding to different pixel
                      coordinates for the same data cube. In such case, pass the data cube in the
                      function parameter 'file' instead of file name. (default False)
    :return: If cli is set as False, returns the spectral signature as a list. Returns error, if any.
    """
    # check if error in skip load
    if skip_load:
        if isinstance(file, str):
            return 6
    else:
        if isinstance(file, ndarray):
            return 7

    result = file if skip_load else load_file(file=file)

    # check if any error while loading file
    if isinstance(result, int):
        return result

    x, y = int(pixel[1]), int(pixel[0])

    try:
        spectral_signature = result[x, y, :]
    except IndexError:
        return 3

    if cli:
        fig, ax = plt.subplots()
        ax.plot(spectral_signature)
        ax.set(xlabel="Bands", ylabel="Intensity", title="Spectral Signature")
        ax.grid()

        plt.show()
    else:
        return spectral_signature
