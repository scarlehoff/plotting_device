import extend_class as ec
import numpy as np

def default_plt():
    import matplotlib.pyplot as plt

    font_family = 'sans-serif'
    font = 'Iosevka'
    text_weight = 'medium'
    label_size = 22
    capsize = 4

    plt.rcParams['font.family'] = font_family
    plt.rcParams['font.sans-serif'] = font
    plt.rcParams['font.weight'] = text_weight
    plt.rcParams['xtick.labelsize'] = label_size
    plt.rcParams['ytick.labelsize'] = label_size
    plt.rcParams['errorbar.capsize'] = capsize

    # Grid
    plt.rcParams['grid.linestyle'] = '--'
    plt.rcParams['grid.linewidth'] = 0.7

    # Generic lines
    plt.rcParams['lines.linewidth'] = 2.0

    # Legend
    plt.rcParams['legend.fontsize'] = label_size-4
    plt.rcParams['legend.frameon'] = False

    # Axes
    plt.rcParams['axes.linewidth'] = 2.2
    plt.rcParams['axes.labelsize'] = label_size
    plt.rcParams['axes.titlesize'] = label_size 

    # Ticks
    plt.rcParams['xtick.direction'] = "in"
    plt.rcParams['ytick.direction'] = "in"


#     plt.rcParams['text.usetex'] = False

    return plt

def draw_canvas(plt, nrows = 2, ncols = 1, gridspec_kw = None, sharex = True, multiscales = False): 
    """
    Call subplots to draw canvas using the gridspec_kw dictionary
    If multiscales, creates a twinx for each axis, numbered at the end of the normal axis list
            ie, if there is 4 subplots, the twinx plots indices are axis[4] for axis[0], 5 for 1, etc.
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
    else:
        axis = [ec.extend_all(axis)]
    if multiscales:
        tmp = []
        for axe in axis:
            tmp_axe = axe.twinx()
            tmp.append(ec.extend_all(tmp_axe))
        axis += tmp

    return fig, axis

def canvas_plot_and_ratio(plt, ratio = [1.5,1], ratio_range = (0.5,1.5), n_ticks = 4, format_tick = "%.0f", keep_limits = False, mode = 'landscape', size = None):
    """
    Create a figure for a plot-ratio 
    ratio: ratio between proper plot and ratio_plot (default, plot 1.5 times bigger than ratio, [1.5,1])
    ratio_range: yrange for ratio plot (default 0.5 to 1.5)
    n_ticks: how many ticks to print
    format_tick: default format tick for plot (default %.0f)
    """
    if size:
        rit = size[0]
        top = size[1]
    if mode == 'landscape':
        if not size:
            rit = 2.0
            top = 1.0
    elif mode == 'portrait':
        if not size:
            rit = 0.9
            top = 2.4
    else:
        if not size:
            rit = 2.0
    from matplotlib.ticker import FormatStrFormatter
    gridspec_kw = { 'height_ratios' : ratio, 'hspace' : 0,
            'left' : 0.0, 'right' : rit, 'bottom' : 0.0, 'top' : top }
    fig, axis = draw_canvas(plt, 2, 1, gridspec_kw = gridspec_kw)

    axis[0].yaxis.set_major_formatter(FormatStrFormatter(format_tick))

    # Generate the first set of limits for the ratio plot with the axis.relimit function from extend_class
    axis[1].keep_limits = False
    axis[1].relimit(n_ticks = n_ticks, line_one = True, padding = 1.05, enforce_lims = ratio_range)

    return fig, axis
    

def save_to_file(fig, filename):
    fig.savefig(filename, bbox_inches = 'tight')

