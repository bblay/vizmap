# (C) British Crown Copyright 2010 - 2012, Met Office
#
# This file is part of Vizmap.
#
# Vizmap is free software: you can redistribute it and/or modify it under
# the terms of the GNU Lesser General Public License as published by the
# Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Vizmap is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with Vizmap.  If not, see <http://www.gnu.org/licenses/>.


import warnings

import iris


def rename_unknown(cube, field, filename):
    
    # rename unknown grib phenomena
    if isinstance(field, iris.fileformats.grib.GribWrapper):
        if field.edition == 1:
            cube.rename("{} table {} item {}".format(field.centre, field.table2Version,
                                                     field.indicatorOfParameter))
        elif field.edition == 2:
            cube.rename("{} d{} c{} n{}".format(field.centre, field.discipline,
                                                field.parameterCategory,
                                                field.parameterNumber))
    else:
        warnings.warn("This callback deos not yet handle type {}".format(type(field)))
