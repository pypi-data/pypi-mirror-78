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

error_dict = {
    0: ("File Not Found!!", "Critical"),
    1: ("Incorrect color-map!", "Critical"),
    2: ("Incorrect Band number value!", "Critical"),
    3: ("Incorrect pixel co-ordinates!!", "Critical"),
    4: ("No spectral data found in the input file!", "Warning"),
    5: ("Could not load the file. Currently supports only mat files", "Warning"),
    6: (
        "Could not perform skip load. Expected data cube as parameter, got string!",
        "Critical",
    ),
    7: ("Could not perform skip load. Expected string as parameter", "Critical"),
    8: ("Incorrect input for metadata function", "Critical"),
}


def get_error_dict():
    """Returns the complete error dictionary"""
    return error_dict


def get_error_message(error_id):
    """Returns the message corresponding to the specified error id"""
    return error_dict[error_id][0]


def get_error_level(error_id):
    """Returns the error level corresponding to the specified error id"""
    return error_dict[error_id][1]
