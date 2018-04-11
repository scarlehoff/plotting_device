import extend_class as ec
import numpy as np

def default_plt():
    import matplotlib.pyplot as plt

    font_family = 'sans-serif'
    font = 'Iosevka'
    text_weight = 20
    label_size = 22
    capsize = 4

    plt.rcParams['font.family'] = font_family
    #plt.rcParams['font.sans-serif'] = font
    plt.rcParams['font.serif'] = font
    plt.rcParams['font.weight'] = text_weight
    plt.rcParams['axes.labelsize'] = label_size
    plt.rcParams['xtick.labelsize'] = label_size
    plt.rcParams['ytick.labelsize'] = label_size
    plt.rcParams['errorbar.capsize'] = capsize
    plt.rcParams['text.usetex'] = True

    return plt

def draw_canvas(plt, nrows = 2, ncols = 1, gridspec_kw = None, sharex = True): 
    """
    Call subplots to draw canvas using the gridspec_kw dictionary
    """
    if not gridspec_kw: # Use default [1,1,1,1]
        ratios = ncols*nrows*[1]
        gridspec_kw = {
            'height_ratios' : ratios,
            'hspace' : 0,
            'left' : 0.0,
            'right' : 2.0,
            'bottom' : 0.0,
            'top' : 1.0 }
    fig, axis = plt.subplots(nrows, ncols, sharex = sharex, gridspec_kw = gridspec_kw)
    if isinstance(axis, np.ndarray):  
        axis = [ec.extend_all(i) for i in axis]
        return fig, axis
    else:
        axis = ec.extend_all(axis)
        return fig, [axis]

def canvas_plot_and_ratio(plt, ratio = [1.5,1], ratio_range = (0.5,1.5), n_ticks = 4, format_tick = "%.0f", keep_limits = False):
    """
    Create a figure for a plot-ratio 
    ratio: ratio between proper plot and ratio_plot (default, plot 1.5 times bigger than ratio, [1.5,1])
    ratio_range: yrange for ratio plot (default 0.5 to 1.5)
    n_ticks: how many ticks to print
    format_tick: default format tick for plot (default %.0f)
    """
    from matplotlib.ticker import FormatStrFormatter
    gridspec_kw = { 'height_ratios' : ratio, 'hspace' : 0,
            'left' : 0.0, 'right' : 2.0, 'bottom' : 0.0, 'top' : 1.0 }
    fig, axis = draw_canvas(plt, 2, 1, gridspec_kw = gridspec_kw)

    axis[0].yaxis.set_major_formatter(FormatStrFormatter(format_tick))

    # Generate the first set of limits for the ratio plot with the axis.relimit function from extend_class
    axis[1].keep_limits = False
    axis[1].relimit(n_ticks = n_ticks, line_one = True, padding = 1.05, enforce_lims = ratio_range)

    return fig, axis
    


