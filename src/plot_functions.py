import src.extend_class as ec
import numpy as np

def default_plt():
    import matplotlib.pyplot as plt

    font_family = 'sans-serif'
    font = 'Iosevka'
    text_weight = 20
    label_size = 16
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

def draw_canvas(plt, ncols = 2, nrows = 1, gridspec_kw = None, sharex = True): 
    """
    Call subplots to draw canvas using the gridspec_kw dictionary
    """
    if not gridspec_kw: # Use default
        gridspec_kw = {
            'height_ratios' : [1.5, 1],
            'hspace' : 0,
            'left' : 0.0,
            'right' : 1.0,
            'bottom' : 0.0,
            'top' : 1.0 }
    fig, axis = plt.subplots(ncols, nrows, sharex = sharex, gridspec_kw = gridspec_kw)
    axis = [ec.extend_all(i) for i in axis]
    return fig, axis

def canvas_plot_and_ratio(plt, ratio = [1.5,1], yrange = (0.5,1.5), tick_step = 0.2, format_tick = "%.0f"):
    """
    Create a figure for a plot-ratio 
    """
    from matplotlib.ticker import FormatStrFormatter
    gridspec_kw = { 'height_ratios' : [1.5, 1], 'hspace' : 0,
            'left' : 0.0, 'right' : 1.0, 'bottom' : 0.0, 'top' : 1.0 }
    fig, axis = draw_canvas(plt, 2, 1, gridspec_kw = gridspec_kw)

    yticks = np.arange(yrange[0], yrange[1]*1.05, tick_step)
    ylabels = [np.around(i,decimals=1) for i in yticks[:-1]]

    yticks = np.append(yticks[:-1], 1.0)
    ylabels.append(1)

    axis[0].yaxis.set_major_formatter(FormatStrFormatter(format_tick))

    axis[1].set_ylim(yrange)
    axis[1].set_yticks(yticks)
    axis[1].set_yticklabels(ylabels)
    axis[1].axhline(y=1, color="black", lw = 1.0)
    
    return fig, axis
    


