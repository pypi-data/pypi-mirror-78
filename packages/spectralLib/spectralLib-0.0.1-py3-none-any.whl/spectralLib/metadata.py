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

from os import path

from numpy import amax, amin, mean

from spectralLib.load.file import load_file

properties_list = [
    "File Name",
    "File Size",
    "Height",
    "Width",
    "No: of Bands",
    "Max. Intensity of Current Band",
    "Min. Intensity of Current Band",
    "Mean Intensity of Current Band",
]


def get_properties_list():
    """Returns the list of properties"""
    return properties_list


def file_size_estimate(file_size):
    """Convert the input file size to best estimate"""
    for x in ["Bytes", "KiB", "MiB", "GiB", "TiB", "PiB"]:
        if file_size < 1024.0:
            return f"{file_size:.1f} {x}"
        file_size /= 1024.0


def get_metadata(input, band_number=0):
    """Returns a dictionary containing metadata or error code if any error occurs.

    :param input: Tuple containing file name and spectral data cube or just file name. If only
                  file name is provided, will load the data cube.
    :param band_number: current band number (default 0)
    :return: metadata dictionary or error code
    """
    if isinstance(input, tuple):
        file_name, datacube = input
    elif isinstance(input, str):
        file_name = input
        datacube = load_file(file=file_name)
    else:
        return 8

    try:
        metadata = [
            path.basename(file_name),
            file_size_estimate(path.getsize(file_name)),
            str(datacube.shape[0]),
            str(datacube.shape[1]),
            str(datacube.shape[2]),
            str(amax(datacube[:, :, band_number])),
            str(amin(datacube[:, :, band_number])),
            str(mean(datacube[:, :, band_number])),
        ]
    except IndexError:
        return 3

    return metadata
