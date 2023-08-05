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

import os

from spectralLib.load.mat import load_mat_file


def load_file(file):
    """Load file based on extension

    :param file: Input file
    :return: Loaded data or error, if any
    """
    if not os.path.isfile(file):
        return 0
    file_name, file_extension = os.path.splitext(file)

    if file_extension == ".mat":
        return load_mat_file(file=file)
    else:
        return 5
