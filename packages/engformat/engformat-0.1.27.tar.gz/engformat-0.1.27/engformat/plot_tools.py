__author__ = 'maximmillen'
from matplotlib.collections import LineCollection
from matplotlib.lines import Line2D
from matplotlib import patches as mpatches
import matplotlib.transforms
import numpy as np

from bwplot import cbox


def trim_ticks(sub_plot, **kwargs):
    balance = kwargs.get('balance', False)
    xlims = sub_plot.get_xlim()
    xticks = list(sub_plot.get_xticks())
    pts = len(xticks)
    for i in range(pts - 1, 0, -1):
        if xticks[i] < xlims[0] or xticks[i] > xlims[1]:
            xticks.pop(i)
    sub_plot.set_xticks(xticks)

    ylims = sub_plot.get_ylim()
    yticks = list(sub_plot.get_yticks())
    pts = len(yticks)
    for i in range(pts - 1, 0, -1):
        if yticks[i] < ylims[0] or yticks[i] > ylims[1]:
            yticks.pop(i)
    if balance and (yticks[0] / -yticks[-1]) - 1.0 > 0.001:
        max_end = np.max([abs(yticks[0]), abs(yticks[-1])])
        tick_delta = abs(yticks[1] - yticks[0])
        yticks = np.arange(-max_end, max_end + tick_delta, tick_delta)
    sub_plot.set_yticks(yticks)


def create_custom_legend_line(label, ls, c, mk, ms=5, mfc=None):
    if mfc is None:
        mfc = c
    return Line2D([0], [0], ls=ls, marker=mk, color=c, label=label,
               markerfacecolor=mfc, markersize=ms)

def create_custom_legend_patch(label, c, alpha=1):
    return mpatches.Patch(color=c, label=label, alpha=alpha)


def revamp_legend(sub_plot, ncol=1, **kwargs):
    loc = kwargs.get('loc', 'upper right')
    single = kwargs.get('single', True)
    bbox_to_anchor = kwargs.get('bbox_to_anchor', False)
    prop = kwargs.get('prop', None)
    add_handles = kwargs.get("add_handles", [])
    fixed_color = kwargs.get('fixed_color', None)

    if single:
        handles, labels = sub_plot.get_legend_handles_labels()
        labs = []
        hands = []
        for qq in range(len(labels)):
            if labels[qq] not in labs:
                labs.append(labels[qq])
                if fixed_color:
                    handles[qq].set_color(fixed_color)
                hands.append(handles[qq])
        for hand in add_handles:
            labs.append(hand.get_label())
            hands.append(hand)

    else:
        hands, labs = sub_plot.get_legend_handles_labels()

    if bbox_to_anchor != False:
        sub_plot.legend(hands, labs, numpoints=1, handlelength=1, handletextpad=0.5, labelspacing=0.3, scatterpoints=1,
                        loc=loc, ncol=ncol, bbox_to_anchor=bbox_to_anchor, prop=prop)
    else:
        sub_plot.legend(hands, labs, numpoints=1, handlelength=1, handletextpad=0.5, labelspacing=0.3, scatterpoints=1,
                        loc=loc, ncol=ncol, prop=prop)
    # borderpad    the fractional whitespace inside the legend border
    # shadow    if True, draw a shadow behind legend
    # framealpha    If not None, alpha channel for the frame.
    # ncol    number of columns
    # labelspacing    the vertical space between the legend entries
    # handlelength    the length of the legend handles
    # handletextpad    the pad between the legend handle and text
    leg = sub_plot.get_legend()


    try:  # check if plot has a legend
        frame = leg.get_frame()
    except AttributeError:
        return

    # leg.set_fancybox(True)
    ltext = leg.get_texts()  # all the text.Text instance in the legend
    # llines = leg.get_lines()  # all the lines.Line2D instance in the legend
    frame.set_lw(0.5)
    frame.set_facecolor('0.99')
    frame.set_edgecolor('0.3')
    frame.set_alpha(kwargs.get('alpha', 1.0))
    for tt in ltext:
        tt.set_color('0.1')
        # tt.set_size(7)
    return leg


def restyle_lines(sub_plot, style="bw", **kwargs):
    """
    Change the color and line style based on the bw_plot style.
    """

    if style == "bw":
        from bwplot import cbox as cs
    elif style == "spectra":
        from bwplot import spectra as cs

    lines = sub_plot.lines
    labs = {}
    cc_box = 0
    for i in range(len(lines)):
        label = lines[i].get_label()
        if "_line" == label[:5]:
            continue  # Don't recolor unlabelled lines

        if label not in labs:  # unique color for each label
            labs[label] = cc_box
            cc_box += 1
        lines[i].set_color(cs(labs[label]))


def text_at_rel_pos(subplot, x, y, text, valign='center', halign='center', color='k'):
    subplot.text(x, y, text,
                       verticalalignment=valign, horizontalalignment=halign,
                       transform=subplot.transAxes,
                       color=color, fontsize=8)


def letter_code(subplots, loc="upper left", col=None):
    """
    Adds a letter from a to z to the corner of each subplot.
    """
    subplots = np.array(subplots)
    nps = len(subplots)
    if loc == "upper left":
        x = 0.03 * np.ones(nps)
        y = 0.95 * np.ones(nps)
    elif loc == "upper right":
        x = 0.85 * np.ones(nps)
        y = 0.98 * np.ones(nps)
    elif loc == "lower left":
        x = 0.03 * np.ones(nps)
        y = 0.5 * np.ones(nps)
    elif loc == "lower right":
        x = 0.03 * np.ones(nps)
        y = 0.5 * np.ones(nps)
    else:
        x = loc[0]
        y = loc[1]

    letters = "abcdefghijklmnopqrstuvwxyz"
    flat_plots = subplots.flatten()
    if col is None:
        col = [1] * len(subplots)
    else:
        assert len(col) == len(flat_plots)
    for i in range(len(subplots)):
        if col[i]:
            color = 'black'
        else:
            color = 'white'
        flat_plots[i].text(x[i], y[i], '(%s)' % letters[i],
            verticalalignment='top', horizontalalignment='left',
            transform=flat_plots[i].transAxes,
            color=color, fontsize=8)


def clean_chart(ax):
    """
    Removes extra lines of axes and tick marks from chart.
    """
    edges = ['top', 'bottom', 'right', 'left']
    ax.tick_params(color=cbox('dark gray'))
    for edge in edges:
        ax.spines[edge].set_color(cbox('dark gray'))
        ax.spines[edge].set_linewidth(0.4)
    ax.yaxis.label.set_color(cbox('dark gray'))
    ax.xaxis.label.set_color(cbox('dark gray'))
    ax.tick_params(axis='x', colors=(0.05, 0.05, 0.05), width=0.5, which='major', top=True)
    ax.tick_params(axis='y', colors=(0.05, 0.05, 0.05), width=0.5, which='major', left=True)


def plot_multicolor_line(splot, x, y, z, cmap=None, vmin=None, vmax=None, lw=None, label=None, off_x=0, off_y=0):
    """
    Adds a line to a plot that changes color based on the z-value and a cmap (default=viridis)
    """
    # Based on the matplotlib example: https://matplotlib.org/gallery/lines_bars_and_markers/multicolored_line.html
    points = np.array([x, y]).T.reshape(-1, 1, 2)
    segments = np.concatenate([points[:-1], points[1:]], axis=1)
    xo = np.ones(len(segments)) * off_x
    yo = np.ones(len(segments)) * off_y
    # xyo = list(zip(xo, yo))
    xyo = np.array([xo, yo]).T
    lc = LineCollection(segments, cmap=cmap, offsets=xyo, transOffset=matplotlib.transforms.IdentityTransform())
    lc.set_array(z)
    lc.set_clim(vmin=vmin, vmax=vmax)
    if lw is not None:
        lc.set_linewidth(lw)
    if label is not None:
        lc.set_label(label)
    return splot.add_collection(lc)


def add_cmap_background(splot, cmap, vmin, vmax, ory='x', se=(0, 1)):
    """
    Adds a background image based on a cmap
    """
    gradient = np.linspace(0, vmin, vmax)

    # gradient = np.linspace(0, 1, 256)
    gradient = np.vstack((gradient, gradient))
    if ory == 'x':
        extent = (vmin, vmax, se[0], se[1])
    else:
        extent = (se[0], se[1], vmin, vmax)
        gradient = gradient.T
    splot.imshow(gradient, aspect='auto', cmap=cmap, vmin=vmin, vmax=vmax, extent=extent)


def plot_std_dev_bounds_vs_x(sps, x, y, xspace=15, pcol='blue', scol='orange'):

    if min(x) == max(x):
        return
    bins = np.linspace(min(x), max(x), xspace)
    try:
        nav, _ = np.histogram(x, bins=bins)
    except ValueError:
        return
    pps = list(nav)
    if pps.count(0) < 8:
        sy, _ = np.histogram(x, bins=bins, weights=y)
        sy2, _ = np.histogram(x, bins=bins, weights=y * y)
        mean = sy / nav
        std = np.sqrt(sy2 / nav - mean * mean)
        xxx = (_[1:] + _[:-1]) / 2
        base = []
        h1 = []
        m_new = []
        h2 = []
        cc = 0
        no_dist = 0
        for u in range(len(std)):
            if np.isnan(std[u]):
                cc += 0  # change this to 1 if you want limit
            else:
                base.append(xxx[u])
                h1.append(mean[u] - std[u])
                m_new.append(mean[u])
                h2.append(mean[u] + std[u])
                cc = 0
            if cc >= 2:
                no_dist = 1
        if no_dist == 0:
            sps.plot(base, m_new, c=pcol, label='Mean')
            sps.fill_between(base, h1, h2, facecolor=scol, alpha=0.3)
            sps.plot(base, h1, c=scol, alpha=0.5, label='Std dev.')
            sps.plot(base, h2, c=scol, alpha=0.5)


def get_percentile_vs_x(x, y, q=25, nbins=15, sorted=True):
    bins = np.linspace(min(x), max(x), nbins + 1)

    if not sorted:
        inds = np.argsort(x)
        x = x[inds]
        y = y[inds]

    inds = np.digitize(x, bins[1:], right=True)  # assume x data is sorted
    base = []
    h1 = []
    m_new = []
    h2 = []
    cc = 0
    no_dist = 0
    for j in range(0, nbins):
        lh = np.searchsorted(inds, j, side='left')
        rh = np.searchsorted(inds, j, side='right')

        if lh == rh:
            cc += 0  # change this to 1 if you want limit
        else:
            vals = y[lh:rh]
            xxx = (x[lh:lh+1][0] + x[rh-1:rh][0]) / 2
            median = np.median(vals)
            p_lb = np.percentile(vals, q)
            p_ub = np.percentile(vals, 100 - q)

            base.append(xxx)
            h1.append(p_lb)
            m_new.append(median)
            h2.append(p_ub)
            cc = 0
    return np.array(base), np.array(m_new), np.array(h1), np.array(h2)


def plot_percentile_bounds_vs_x(sps, x, y, q=25, nbins=15, pcol='blue', scol='orange', sorted=True, line_alpha=1):
    """
    Plots the q and 100-q as well as the median

    :param sps:
    :param x:
    :param y:
    :param q: float
        Percentage
    :param xspace:
    :param pcol:
    :param scol:
    :return:
    """
    if min(x) == max(x):
        return
    bins = np.linspace(min(x), max(x), nbins + 1)

    if not sorted:
        inds = np.argsort(x)
        x = x[inds]
        y = y[inds]

    inds = np.digitize(x, bins[1:], right=True)  # assume x data is sorted
    base = []
    h1 = []
    m_new = []
    h2 = []
    cc = 0
    no_dist = 0
    for j in range(0, nbins):
        lh = np.searchsorted(inds, j, side='left')
        rh = np.searchsorted(inds, j, side='right')

        if lh == rh:
            cc += 0  # change this to 1 if you want limit
        else:
            vals = y[lh:rh]
            xxx = (x[lh:lh+1][0] + x[rh-1:rh][0]) / 2
            median = np.median(vals)
            p_lb = np.percentile(vals, q)
            p_ub = np.percentile(vals, 100 - q)

            base.append(xxx)
            h1.append(p_lb)
            m_new.append(median)
            h2.append(p_ub)
            cc = 0
        if cc >= 2:
            no_dist = 1
    if no_dist == 0:
        sps.plot(base, m_new, c=pcol, label='Mean')
        sps.fill_between(base, h1, h2, facecolor=scol, alpha=0.3)
        lab = f'{q} - {100-q} %'
        sps.plot(base, h1, c=scol, alpha=line_alpha, label=lab)
        sps.plot(base, h2, c=scol, alpha=line_alpha)


def run_plot_percentile_bounds():
    x = [1, 1, 1, 3, 3, 5, 5, 5]
    y = np.arange(len(x))
    import matplotlib.pyplot as plt
    bf, sps = plt.subplots()
    plot_percentile_bounds_vs_x(sps, x, y, 25, nbins=3)
    plt.show()


if __name__ == '__main__':
    run_plot_percentile_bounds()
