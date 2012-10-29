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


import glob

import iris


def slicer(cubes):
    # Turn a sequence of cubes into a sequence of latlon slices. 
    for cube in cubes:
        for slice in cube.slices(["latitude", "longitude"]):
             yield slice


def filespecs_cubes(filespecs, raw, constraints, callback=None):
    # Return cubes from filespecs.
    for filespec in filespecs:
        print "filespec:", filespec
        # Return cubes from filespec. Could be multiple files and cubes.
        for filename in glob.iglob(filespec):
            if filename != filespec:
                print "  filename:", filename
            
            if raw is True:
                cubes = iris.load_raw(filename, constraints=constraints, callback=callback)
            else:
                cubes = iris.load_cubes(filename, constraints=constraints, callback=callback)
        
            for cube in cubes:
                yield cube
