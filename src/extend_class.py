# Methods that extend matplotlib

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
def draw_boxxyerrorbar(axis, plot, alpha=0.25):
    """
    Gnuplot-like errorbars
    """
    from matplotlib.collections import PatchCollection
    r = boxxyerrorbar(plot.xmin, plot.xmax, plot.ymin, plot.ymax)
    pc = PatchCollection(r, facecolor=plot.color, 
                         edgecolor='None', alpha=alpha)
    axis.add_collection(pc)

def gnu_errorbar(axis, plot, padding = 1.05, show_legend = True):
    cur_ylim = axis.get_ylim()
    axis.set_ylim( (min(cur_ylim[0], min(plot.ymin)), max(cur_ylim[1], padding*max(plot.ymax))) )
    cur_xlim = axis.get_xlim()
    axis.set_xlim( (min(cur_xlim[0], min(plot.xmin)), max(cur_xlim[1], max(plot.xmax))) )
    axis.errorbar(plot.x, plot.y, yerr=plot.stat_err, label=plot.legend, fmt=plot.fmt)
    if plot.xlabel: axis.set_xlabel(plot.xlabel)
    if plot.xlabel: axis.set_xlabel(plot.xlabel)
    if plot.ylabel: axis.set_ylabel(plot.ylabel)
    if plot.legend and show_legend: axis.legend()
    axis.grid(linestyle = '--')


def extend_all(plt):
    from types import MethodType
    plt.draw_boxxyerrorbar = MethodType(draw_boxxyerrorbar, plt)
    plt.gnu_errorbar = MethodType(gnu_errorbar, plt)
    return plt
