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


def display_spectral_image(
    file, band_number=0, cmap="viridis", cli=True, skip_load=False
):
    """Display spectral image from input file


    :param file: Input file - file name or data cube
    :param band_number: Band number of data to be displayed (default 0)
    :param cmap: Color map of the plot (default viridis)
    :param cli: Boolean variable. If set as True, displays the image in matplotlib window.
                If set as False, returns the image as a ndarray object. The GUI app using
                this library can display the image using this data. (default True)
    :param skip_load: Boolean variable. If set as True, skips loading the dataset (To improve
                      performance, if data is already loaded). Can be used when calling this
                      function to display spectral image corresponding to different band numbers
                      for the same data cube. In such case, pass the data cube in the function
                      parameter 'file' instead of file name. (default False)
    :return: If cli is set as False, returns the spectral image as a ndarray object.
             Returns error, if any
    """
    # check if cmap is valid
    if cmap not in plt.colormaps():
        return 1

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

    # check if band_number is valid
    if band_number not in range(result.shape[2]):
        return 2

    spectral_image = result[:, :, band_number]

    if cli:
        plt.set_cmap(cmap)
        plt.imshow(spectral_image)
        plt.colorbar()
        plt.show()
    else:
        return spectral_image
