#!/usr/bin/env python3

import numpy as np
import src.my_maths as mm
from pdb import set_trace as dbg

class Plot:

    """ In its more general representation, a plot is made of 7 arrays and a filename:
    x, xmin, xmax
    y, ymin, ymax, stat_err

    It can be initialised with a filename, giving the columns that corresponds to each data

    or from a dataset, directly inputing the columns
    [x, xmin, xmax]
    [y, ymin, ymax, ymin, ymax, ymin, ymax, ... , stat_err]
    everything other than x and y is optional
    """

    def __init__(self, filename = None, columns_x = [0,1,2], columns_y = [3,4,5,6], 
            x_data = None, y_data = None):
        self.xlabel = None  
        self.ylabel = None
        self.legend = None   
        self.fmt = "."
        self.color = None  
        if filename:
            self.filename = filename
            self._unpack_from_file(filename, columns_x, columns_y)
        elif x_data and y_data:
            self.filename = "Derived plot"
            self._unpack_from_data(x_data, y_data)
        else:
            raise Exception("Read the documentation for this software you prick")
        self._cook_data()

    # Setters

    def set_label_parameters(self, xlabel = None, ylabel = None, legend = None):
        if xlabel: self.xlabel = xlabel
        if ylabel: 
            self.ylabel = ylabel
        if legend: self.legend = legend

    def set_plot_parameters(self, color = 'blue', marker = '.', line = '', fmt = None):
        self.color = color
        if fmt:
            self.fmt = fmt
        else:
            self.fmt = "{0}{1}".format(marker, line)

    def _print(self, msg):
        if not self.quiet:
            print(msg)

    def _create_envelope(self, arrays):
        """
        From some set of arrays it returns a central value, a minimum and maximum
        """
        la = len(arrays)
        center = np.array(arrays[0])
        if la == 1:
            min_arr = np.array(arrays[0])
            max_arr = np.array(arrays[0])
        elif la == 2:
            error = np.array(arrays[1])
            min_arr = center - error
            max_arr = center + error
        else:
            max_l = []
            min_l = []
            n_points = len(center)
            if la % 2 == 0:
                error = np.array(arrays[-1])
                la_wo = la-1
            else:
                error = np.zeros(n_points)
                la_wo = la
            for i in range(n_points):
                l = [array[i] for array in arrays[1:la_wo]]
                max_l.append(max(max(l), center[i]+error[i]))
                min_l.append(min(min(l), center[i]-error[i]))
            min_arr = np.array(min_l)
            max_arr = np.array(max_l)
        return center, min_arr, max_arr

    def _unpack_from_file(self, filename, columns_x, columns_y, comments = ["#", "@"]):
        """
        Given a file name, uses np.loadtxt to open it and load it to the x, x_min, x_max (and y) members
        columns_x = [x, xmin, xmax]
        columns_y = [y, ymin, ymax, ymin2, ymax2, ..., stat_err] 
                    all but x and y are optional
        if only two columns are used in x or y: min/max = columns[0]-/+columns[1]
        if only one column is given in x, xmin/max = x -/+ Delta_x with Delta_x distance between 2 adjacent points
        if only one column is given in y, ymin=ymax=y
        Note: it could happen that a member of ymin is greater than a member of ymax
            we will shift members around to avoid that
        """
        columns_x = list(columns_x)
        columns_y = list(columns_y)
        last_col = max(columns_x + columns_y)
        data = np.loadtxt(filename, comments=comments, usecols=range(last_col + 1), unpack=True)

        self.x, self.xmin, self.xmax = self._create_envelope(data[columns_x])
        self.y, self.ymin, self.ymax = self._create_envelope(data[columns_y])

        if len(columns_y) % 2 == 0:
            self.stat_err = data[columns_y[-1]]
        else:
            self.stat_err = np.zeros(len(self.x))


    def _unpack_from_data(self, x_data, y_data):
        """
        Simply upacks 
        x_data = [x, xmin, xmax]
        if len(columns_y) == 2 or len(columns_y) == 4:
            self.stat_err = data[columns_y[-1]]
        else:
            self.stat_err = np.zeros(len(self.x))
        y_data = [y, ymin, ymax, stat_err] 
        everything but the central values (x,y) are optional, see _unpack_from_file for details
        """
        self.x, self.xmin, self.xmax = self._create_envelope(x_data)
        self.y, self.ymin, self.ymax = self._create_envelope(y_data)

        if len(y_data) % 2 == 0:
            self.stat_err = y_data[-1]
        else:
            self.stat_err = np.zeros(len(self.x))

    def _cook_data(self):
        """
        Ensures xmin/xmax actually make sense
        """

        if np.array_equal(self.xmin, self.xmax):
            delta = (self.x[-1] - self.x[0])/(len(self.x)-1.0)
            self.xmin = np.array([i-delta/2.0 for i in self.x])
            self.xmax = np.array([i+delta/2.0 for i in self.x])



    # Output functions

    def get_integral(self, xmin = None, xmax = None):
        if not xmin:
            xmin = self.xmin[0]
        if not xmax:
            xmax = self.xmax[-1]

        dy = self.stat_err[ (self.x >= xmin) & (self.x <= xmax) ]
        total_dy = np.sqrt(sum([i*i for i in dy]))

        total_y = 0
        for xm,xp,y in zip(self.xmin, self.xmax, self.y):
            if (xm >= xmin) & (xp <= xmax):
                total_y += y*(xp-xm)
        return total_y, total_dy


    def get_total(self, xmin = None, xmax = None):
        if not xmin:
            xmin = self.xmin[0]
        if not xmax:
            xmax = self.xmax[-1]

        y = self.y[ (self.x >= xmin) & (self.x <= xmax) ]
        dy = self.stat_err[ (self.x >= xmin) & (self.x <= xmax) ]

        total_y = sum(self.y[ (self.x >= xmin) & (self.x <= xmax) ])
        total_dy = np.sqrt(sum([i*i for i in dy]))

        return total_y, total_dy


    def output_columns(self):
        """
        Outputs plot data
        xmin x xmax y ymin ymax y_stat_err
        """
        zipi = zip(self.xmin, self.x, self.xmax, self.y, self.ymax, self.ymin, self.stat_err)
        for data in zipi:
            data_str = [str(i) for i in data]
            print(" ".join(data_str))

    # Overloads
    def __str__(self):
        return "Plot object for '{0}'".format(self.filename)

    def __truediv__(self, divider): 
        if isinstance(divider, type(self)): # Ratio self / plot
            plot = divider
            # Step 1, check that the x axis is the same in both plots
            if not np.array_equal(self.x, plot.x):
                raise Exception("You are trying to take the ratio of two plots with different x axis")
            x_data = [self.x, self.xmin, self.xmax]
            # Take ratio of central values
            min_y = [mm.divide(i,j) for i,j in zip(self.ymin, plot.y)]
            max_y = [mm.divide(i,j) for i,j in zip(self.ymax, plot.y)]
            central_y = []
            central_dy = []
            for i,j, di,dj in zip(self.y, plot.y, self.stat_err, plot.stat_err):
                y,dy = mm.division_w_err(i,j, da=di,db=dj)
                central_y.append(y)
                central_dy.append(dy)
            y_data = [central_y, min_y, max_y, central_dy]
            new_plot = Plot(x_data = x_data, y_data = y_data)
            new_plot.set_label_parameters(legend = "{0}/{1}".format(self.legend, plot.legend))
            new_plot.set_label_parameters(xlabel = self.xlabel)
            new_plot.set_plot_parameters(fmt = self.fmt, color = self.color)
        elif isinstance(divider, float):
            import copy
            new_plot = copy.copy(self)
            new_plot.y = self.y/divider
            new_plot.ymin = self.ymin/divider
            new_plot.ymax = self.ymax/divider
            new_plot.stat_err = self.stat_err/divider
        elif isinstance(divider, (tuple,list)):
            import copy
            new_plot = copy.copy(self)
            new_plot.ymin = self.ymin/divider[0]
            new_plot.ymax = self.ymax/divider[0]
            central_y = []
            central_dy = []
            for i, di in zip(self.y, self.stat_err):
                y,dy = mm.division_w_err(i,divider[0], da=di,db=divider[1])
                central_y.append(y)
                central_dy.append(dy)
            new_plot.y = central_y
            new_plot.stat_err = central_dy
        else:
            raise Exception("Division between types 'Plot' and '{0}' not implemented".format(type(divider)))
        return new_plot

        
if __name__ == "__main__":
    file1 = "test1.dat"
    file2 = "test2.dat"

    xcol = [1,0,2]
    ycol = [3,4]

    plot1 = Plot(file1, xcol, ycol)
    plot2 = Plot(file2, xcol, ycol)

    print(plot1.get_total())
    print(plot2.get_total())


    plot1.output_columns()




