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


import time

import matplotlib.pyplot as plt
import iris.quickplot as qplt
import numpy


def _viz_slice(slice, subplot, cmap):
    # Plot a latlon slice in a given subplot position.
    ax = plt.subplot(*subplot)
    
    # If we're using pcolormesh we need bounds
    if not slice.coord("latitude").has_bounds():
        slice.coord("latitude").guess_bounds()
        slice.coord("longitude").guess_bounds()
    
    # How many ticks along the colourbar?
    # Depends on the number of subplots.
    if subplot[0] == 1:
        num_ticks = None
    elif subplot[0] == 2:
        num_ticks = 8
    elif subplot[0] == 3:
        num_ticks = 6
    else:
        num_ticks = 5
    
    qplt.pcolormesh(slice, num_ticks=num_ticks)
    plt.gca().coastlines()


class Visualiser(object):
    """Plots latlon slices from a sequence of cubes in an nxn grid."""
    
    def __init__(self, slices, size, num_subplots, cmap):
        self.slices = slices
        self.size = size
        self.num_subplots = num_subplots
        self.cmap = cmap
        self.fig = plt.figure(figsize=self.size)
        
    def _viz_slices(self):
        # Add the keypress handler and show the window
        self.fig.canvas.mpl_connect('key_press_event', self._viz_bunch)
        self._viz_bunch(None)
        plt.show()
        print "finished"

    def _viz_bunch(self, event):
        # Plot the next n slices
        self.fig.clf()
        
        # Try and get up to the next n slices.
        if self.num_subplots is None:
            n = 9
        else:
            n = numpy.product(self.num_subplots)
            
        bunch = []
        for i in range(n):
            try:
                bunch.append(self.slices.next())
            except StopIteration:
                break
    
        if len(bunch) == 0:
            plt.close()
            return
        
        # How many subplots? (persists throughout the lifetime of this object)
        if self.num_subplots is None:
            self.num_subplots = self.how_many_subplots(len(bunch))
    
        print "plotting"
        start_time = time.time()
    
        # Plot this bunch of slices    
        # TODO: Subplot multiprocessing doesn't work. Raise a mpl issue?
        for i, slice in enumerate(bunch):
            subplot = self.num_subplots + tuple([i+1])
            _viz_slice(slice, subplot, self.cmap)
    
        print "Plotted {} slices in {:.1f}s".format(len(bunch), time.time() - start_time)
        
        # Show the plots and wait for a keypress
        self.fig.canvas.draw()
        
    @staticmethod
    def how_many_subplots(num):
        """Decide how many subplots we should use for n slices."""
        if num == 1:
            result = (1,1)
        elif num == 2:
            result = (2,1)
        elif num <= 4:
            result = (2,2)
        elif num <= 6:
            result = (3,2)
        else:
            result = (3,3)
        return result
    
   