import src.extend_class as ec
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
            'right' : 1.0,
            'bottom' : 0.0,
            'top' : 1.0 }
    fig, axis = plt.subplots(nrows, ncols, sharex = sharex, gridspec_kw = gridspec_kw)
    if isinstance(axis, np.ndarray):  
        axis = [ec.extend_all(i) for i in axis]
        return fig, axis
    else:
        axis = ec.extend_all(axis)
        return fig, [axis]

def canvas_plot_and_ratio(plt, ratio = [1.5,1], ratio_range = (0.5,1.5), tick_step = 0.2, format_tick = "%.0f"):
    """
    Create a figure for a plot-ratio 
    ratio: ratio between proper plot and ratio_plot (default, plot 1.5 times bigger than ratio, [1.5,1])
    ratio_range: yrange for ratio plot (default 0.5 to 1.5)
    tick_step: default tick step for ratio plot (default 0.2)
    format_tick: default format tick for plot (default %.0f)
    """
    from matplotlib.ticker import FormatStrFormatter
    gridspec_kw = { 'height_ratios' : [1.5, 1], 'hspace' : 0,
            'left' : 0.0, 'right' : 1.0, 'bottom' : 0.0, 'top' : 1.0 }
    fig, axis = draw_canvas(plt, 2, 1, gridspec_kw = gridspec_kw)

    yticks = np.arange(ratio_range[0], ratio_range[1]*1.05, tick_step)
    ylabels = [np.around(i,decimals=1) for i in yticks[:-1]]

    yticks = np.append(yticks[:-1], 1.0)
    ylabels.append(1)

    axis[0].yaxis.set_major_formatter(FormatStrFormatter(format_tick))

    axis[1].set_ylim(ratio_range)
    axis[1].set_yticks(yticks)
    axis[1].set_yticklabels(ylabels)
    axis[1].axhline(y=1, color="black", lw = 1.0)
    
    return fig, axis
    


