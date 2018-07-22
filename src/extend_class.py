# Methods that extend matplotlib
from NewNumber import NewNumber
import numpy as np

def update_limits(axis, plot, padding = 0.05):
    """
        Update the limits on the axis of the plot (with a padding from the top of 'padding')
        It looks at the previous limits and enlarge them but never shrinks them
    """
    if axis.keep_limits:
        return
    try:
        if axis.gnu_extended_object == "new":
            axis.gnu_extended_object = "old"
            cur_ylim = (plot.y[0], plot.y[0])
            cur_xlim = (plot.x[0], plot.x[0])
        else:
            cur_ylim = axis.get_ylim()
            cur_xlim = axis.get_xlim()
    except:
        raise Exception("Object type: {0} didn't have property gnu_extended_object set. Can't continue".format(type(axis)))
    axis.set_ylim( (min(cur_ylim[0], min(plot.ymin)), max(cur_ylim[1], (1.0+padding)*max(plot.ymax))) )
    axis.set_xlim( (min(cur_xlim[0], min(plot.xmin)), max(cur_xlim[1], max(plot.xmax))) )

def draw_labels(axis, plot, show_legend = True):
    """
        If set in the plot object, draw xlabel, ylabel and legend
    """
    if plot.xlabel: axis.set_xlabel(plot.xlabel, weight = 'medium')
    if plot.ylabel: axis.set_ylabel(plot.ylabel, weight = 'medium')
    if plot.legend and show_legend: 
        axis.legend()


def boxxyerrorbar(xmin, xmax, ymin, ymax):
    from matplotlib.patches import Rectangle
    data = zip(xmin,xmax,ymin,ymax)
    r =[]
    for xm,xp, ym,yp in data:
        r.append(Rectangle(
            (xm,ym), # x,u
            xp-xm, # width
            yp-ym, # height
        ))
    return r
def draw_boxxyerrorbar(axis, plot, alpha=0.25, draw_labels = False):
    """
    Gnuplot-like errorbars
    """
    from matplotlib.collections import PatchCollection
    r = boxxyerrorbar(plot.xmin, plot.xmax, plot.ymin, plot.ymax)
    pc = PatchCollection(r, facecolor=plot.color, 
                         edgecolor='None', alpha=alpha)
    if not plot.color: # maybe the plot did not contain a color, let's give it some color!
        if isinstance(pc, (tuple, list)):
            color = pc[0].get_facecolor()
        else:
            color = pc.get_facecolor()
        # Update the plot color
        plot.set_plot_parameters(color = color)
    if draw_labels:
        axis.draw_labels(plot)
    axis.add_collection(pc)

def gnu_histeps(axis, plot, show_legend = False, draw_labels = True):
    """
    Equivalent to gnuplot histeps. 
    """
    axis.update_limits(plot, padding = 0.05)
   
    # Works surprisingly well for different-size steps *shrug emoji*
    eb = axis.step(plot.xmin, plot.y, where='post', color = plot.color)
    if not plot.color:
        plot.color = eb[0].get_color()
    if show_legend:
        legend = plot.legend
    else:
        legend = None
    axis.step(plot.xmax[-2:], plot.y[-2:], where='pre', color = plot.color, label = legend)
    if draw_labels:
        axis.draw_labels(plot, show_legend)
    if isinstance(show_legend, (str, tuple, list)):
        axis.legend(loc = show_legend)

def gnu_errorbar(axis, plot, padding = 0.05, draw_labels = True, show_legend = True, histeps = False, color = None):
    """
    Plot x, y, dy in a gnuplot-like style
    axis should be a matplotlib axis object 
    plot should be from src.Plot
    
    if histeps = True is selected, gnuplot-like histeps are also printed
    """
    # Set up the limits (make sure we don't override previous limits)
    axis.update_limits(plot, padding = padding)

    # If the plot contains a color and there is no color in the input arguments, use that:
    if not color:
        color = plot.color

    # Plot errorbars
    eb = axis.errorbar(plot.x, plot.y, yerr=plot.stat_err, label=plot.legend, color = color, fmt=plot.fmt)
    if not color: # maybe the plot did not contain a color, let's give it some color!
        color = eb[0].get_color()
        # Update the plot color
        plot.set_plot_parameters(color = color)

    if histeps:
        axis.gnu_histeps(plot, draw_labels = False)

    if draw_labels:
        axis.draw_labels(plot, show_legend)

    axis.grid(linestyle = '--')

def gnu_line(axis, plot, padding = 0.05, draw_labels = True, show_legend = True, histeps = False, color = None):
    """
    Plot x, y, dy in a gnuplot-like style
    axis should be a matplotlib axis object 
    plot should be from src.Plot
    
    if histeps = True is selected, gnuplot-like histeps are also printed
    """
    # Set up the limits (make sure we don't override previous limits)
    axis.update_limits(plot, padding = padding)

    # If the plot contains a color and there is no color in the input arguments, use that:
    if not color:
        color = plot.color

    # Plot errorbars
    eb = axis.plot(plot.x, plot.y, label=plot.legend, color = color)
    if not color: # maybe the plot did not contain a color, let's give it some color!
        color = eb[0].get_color()
        # Update the plot color
        plot.set_plot_parameters(color = color)

    if histeps:
        axis.gnu_histeps(plot, draw_labels = False)

    if draw_labels:
        axis.draw_labels(plot, show_legend)

    axis.grid(linestyle = '--')


def relimit(axis, n_ticks = 4, line_one = False, padding = 1.05, enforce_lims = None):
    """ 
    Tries to figure out ylimits by itself.
    It will also print a line across one if needed and will try to figure out the correct
    separation between ticks
    """
    if enforce_lims:
        ymin = NewNumber(enforce_lims[0])
        ymax = NewNumber(enforce_lims[1])

        pow10 = (ymax-ymin).power_of_10(partition = 3)

    else:
        ymin_l = []
        ymax_l = []
        for line in axis.lines:
            ydata = line.get_ydata()
            ymin_l.append(min(ydata))
            ymax_l.append(max(ydata))

        ymin = min(ymin_l)
        ymax = max(ymax_l)

        pow10 = NewNumber(ymax-ymin).power_of_10(partition = 3)

        rounder = pow(10, pow10)
        ymax = NewNumber(ymax).floor(decimals = -pow10) + rounder
        ymin = NewNumber(ymin).ceil(decimals = -pow10) - rounder

    deltay = ymax - ymin
    t_step = deltay / (n_ticks + 1.0)
    t_step = t_step.ceil(decimals = -pow10)

    yticks = np.arange(ymin.x, ymax.x, t_step.x)
    ylabels = [np.around(i,decimals=-pow10) for i in yticks]

    if line_one:
        axis.axhline(y=1, color="black", lw = 1.0)

        if 1.0 not in yticks:
            yticks = np.append(yticks, 1.0)
            ylabels.append(1)

    d_padding = float(t_step/4.0*padding)

    axis.set_ylim( (ymin.x, ymax.x + d_padding) )
    axis.set_yticklabels(ylabels)
    axis.set_yticks(yticks)


def extend_all(plt):
    from types import MethodType
    plt.draw_boxxyerrorbar = MethodType(draw_boxxyerrorbar, plt)
    plt.gnu_errorbar = MethodType(gnu_errorbar, plt)
    plt.gnu_histeps  = MethodType(gnu_histeps , plt)
    plt.update_limits = MethodType(update_limits, plt)
    plt.draw_labels   = MethodType(draw_labels  , plt)
    plt.gnu_line = MethodType(gnu_line, plt)
    plt.relimit = MethodType(relimit, plt)
    plt.keep_limits = False
    plt.gnu_extended_object = "new"
    return plt
