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


import iris

import slicer
import util
import visualiser


def vizmap(target, size=(12,10), num_subplots=None, cmap=None, pad=None,
           constraints=None, raw=True, callback=None):
    """
    Visualise latlon slices.
    
    Args:
    
        * target          -    Cube, CubeList or filespec (can include wildcards).
     
    Kwargs:
    
        * size            -    Window size. Defaults to (12,10).
        * num_subplots    -    Subplot grid layout, such as (9,9).
                               Decided automatically if None.
        * cmap            -    A matplotlib.colors.Colormap passed to pcolormesh.
        * pad             -    Distance between plot and colorbar.
        * constraints     -    Iris loading constraints.
        * raw             -    Use iris.load_raw() when target is a filespec.
        * callback        -    Run this callback for each loaded cube (pre merge).
        
    """
    
    if pad is None:
        pad=0.03
    
    # Cube
    if isinstance(target, iris.cube.Cube):
        slice_iterator = slicer.slicer([target])
    
    # CubeList or iterable of Cubes
    elif (isinstance(target, iris.cube.CubeList) or
          (hasattr(target, "__iter__") and isinstance(target[0], iris.cube.Cube))):
        slice_iterator = slicer.slicer(target)
    
    # Filespec
    elif isinstance(target, basestring):
        cubes = slicer.filespecs_cubes([target], raw, constraints, callback=callback)
        slice_iterator = slicer.slicer(cubes)
    
    # Iterable of filespecs
    elif hasattr(target, "__iter__") and isinstance(target[0], basestring):
        cubes = slicer.filespecs_cubes(target, raw, constraints, callback=callback)
        slice_iterator = slicer.slicer(cubes)
        
    else:
        raise ValueError("Please provide cube(s) or filename(s)")

    viz = visualiser.Visualiser(slice_iterator, size, num_subplots, cmap, pad)
    viz._viz_slices()


if __name__ == "__main__":

    folder = "/net/home/h05/itbb/git/vizmap/sample_data/aviation/"
    filespec = [folder+"global.grib1", folder+"wave.grib1", folder+"winduv.grib2"]
    vizmap(filespec, callback=util.rename_unknown)
    vizmap(filespec, callback=util.rename_unknown, num_subplots=(1,1))
    vizmap(filespec, callback=util.rename_unknown, num_subplots=(2,2))
    vizmap(filespec, callback=util.rename_unknown, num_subplots=(3,3))
    vizmap(filespec, callback=util.rename_unknown, num_subplots=(4,4))
