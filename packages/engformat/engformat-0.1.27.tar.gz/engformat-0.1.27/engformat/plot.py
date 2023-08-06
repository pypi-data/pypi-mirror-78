__author__ = 'maximmillen'

import pickle

from bwplot import cbox
import numpy as np

import engformat.plot_tools as tools
import matplotlib.pyplot as plt

from matplotlib import rc
# rc('font', family='Helvetica', size=9, weight='light')
# plt.rcParams['pdf.fonttype'] = 42
# plt.rcParams['ps.fonttype'] = 42  # To avoid type 3 fonts
# matplotlib.rcParams['font.family'] = 'Times New Roman'
# matplotlib.rcParams['font.size'] = '9'
# matplotlib.rcParams['font.weight'] = 'light'
import matplotlib


def journal_figure(fig, figure_path, size="small"):
    fig.set_size_inches(4, 4)

    fig.savefig(figure_path, dpi=100)


def time_series(sp, **kwargs):
    balance = kwargs.get('balance', False)
    x_axis = kwargs.get('x_axis', True)
    x_origin = kwargs.get('x_origin', False)
    y_origin = kwargs.get('y_origin', False)
    sp.yaxis.grid(True)
    tools.clean_chart(sp)
    xlim = sp.get_xlim()
    ylim = sp.get_ylim()
    if x_origin:
        sp.set_xlim([0, xlim[1]])
    if y_origin:
        sp.set_ylim([0, ylim[1]])
    if x_axis:
        sp.plot(sp.get_xlim(), [0, 0], c=cbox('dark gray'), ls='--', zorder=-1, lw=0.7)
    if balance:
        ylim = max(abs(sp.get_ylim()[0]), abs(sp.get_ylim()[1]))
        sp.set_ylim([-ylim, ylim])
    sp.tick_params(axis="both", which="both", bottom=True, top=False,
                   labelbottom=True, left=True, right=False, labelleft=True)
    tools.trim_ticks(sp, balance=balance)
    if balance:
        ylim = max(abs(sp.get_ylim()[0]), abs(sp.get_ylim()[1]))
        sp.set_ylim([-ylim, ylim])


def new_time_series_plots(nrows=1):

    bf, sub_plots = plt.subplots(nrows=nrows, ncols=1, sharex=True)
    for sp in sub_plots:
        sp.tick_params(axis="both", which="both", bottom=False, top=False,
                                   labelbottom=True, left=False, right=False, labelleft=True)
    sub_plots[-1].tick_params(axis="both", which="both", bottom=True, top=False,
                   labelbottom=True, left=False, right=False, labelleft=True)
    return sub_plots


def time_series_plots(sub_plots):

    for sp in sub_plots:
        sp.tick_params.tick_params(axis="both", which="both", bottom=False, top=False,
                                   labelbottom=True, left=False, right=False, labelleft=True)
        sp.set_xlabel("")
    sub_plots[-1].tick_params(axis="both", which="both", bottom=True, top=False,
                   labelbottom=True, left=False, right=False, labelleft=True)
    return sub_plots


def xy(sp, **kwargs):
    matplotlib.rcParams['lines.linewidth'] = 1.2
    x_origin = kwargs.get('x_origin', False)
    y_origin = kwargs.get('y_origin', False)
    x_axis = kwargs.get('x_axis', False)
    y_axis = kwargs.get('y_axis', False)
    parity = kwargs.get('parity', False)
    x_grid = kwargs.get('x_grid', False)
    y_grid = kwargs.get('y_grid', False)
    ratio = kwargs.get('ratio', False)
    if x_grid:
        sp.yaxis.grid(True, c=cbox('light gray'), zorder=-500, ls="--")
    if y_grid:
        sp.xaxis.grid(True, c=cbox('light gray'), zorder=-600, ls="--")
    sp.set_axisbelow(True)
    tools.clean_chart(sp)
    sp.tick_params(axis="both", which="both", top=False,
                   right=False)
    xlim = sp.get_xlim()
    ylim = sp.get_ylim()
    if x_origin:
        sp.set_xlim([0, xlim[1]])
    if y_origin:
        sp.set_ylim([0, ylim[1]])
    xlim = sp.get_xlim()
    ylim = sp.get_ylim()
    if x_axis:
        sp.axhline(0, c=cbox('dark gray'), zorder=0.6)
    if y_axis:
        sp.axvline(0, c=cbox('dark gray'), zorder=0.55)
    if ratio:
        sp.plot(xlim, [1, 1], c=cbox('dark gray'), zorder=-3)
    if parity:
        botlim = min(xlim[0], ylim[0])
        toplim = min(xlim[1], ylim[1])
        sp.plot([botlim, toplim], [botlim, toplim], c=cbox('mid gray'), zorder=-2)
        if parity == 2:
            if botlim == 0.0:
                xs = np.linspace(botlim, toplim, 2)
            else:
                xs = np.logspace(np.log10(botlim), np.log10(toplim), 30)
            sp.fill_between(xs, xs * 0.5, xs * 2, facecolor=cbox('mid gray'),
                            zorder=-3, alpha=0.3)
            # sp.plot([0, minlim], [0, 0.5 * minlim], c=cbox('mid gray'), zorder=-2)


def rotation_settlement(sp):
    sp.yaxis.grid(True)
    sp.xaxis.grid(True)
    tools.clean_chart(sp)
    xlim = max(abs(sp.get_xlim()[0]), abs(sp.get_xlim()[1]))
    sp.set_xlim([-xlim, xlim])
    sp.set_ylim([(sp.get_ylim()[0]), (sp.get_ylim()[1])])
    # plot origin
    sp.plot([-xlim, xlim], [0, 0], c=cbox('dark gray'), zorder=-1)
    sp.plot([0, 0], [(sp.get_ylim()[0]), (sp.get_ylim()[1])], c=cbox('dark gray'), zorder=-2)
    sp.tick_params(axis="both", which="both", bottom=True, top=False,
                   labelbottom=True, left=True, right=False, labelleft=True)


def hysteresis(sp):
    sp.yaxis.grid(True)
    sp.xaxis.grid(True)
    tools.clean_chart(sp)
    ylim = max(abs(sp.get_ylim()[0]), abs(sp.get_ylim()[1]))
    sp.set_ylim([-ylim, ylim])
    xlimits = sp.get_xlim()
    xlims = [0, 0]
    for x in range(len(xlimits)):
        if abs(xlimits[x]) > 0.999 and abs(xlimits[x]) < 1.0001:
            xlims[x] = 0
            print('found culprit')
        else:
            xlims[x] = xlimits[x]
    print('xlims: ', xlims)
    xlim = max(abs(xlims[0]), abs(xlims[1]))
    sp.set_xlim([-xlim, xlim])
    # plot origin
    sp.plot([-xlim, xlim], [0, 0], c=cbox('dark gray'), zorder=-1)
    sp.plot([0, 0], [-ylim, ylim], c=cbox('dark gray'), zorder=-2)
    sp.tick_params(axis="both", which="both", bottom=True, top=False,
                   labelbottom=True, left=True, right=False, labelleft=True)


def transfer_function(sp, **kwargs):
    """
    Prepare a transfer function plot
    :param sp:
    :param kwargs:
    :return:
    """

    x_grid = kwargs.get('x_grid', True)
    y_grid = kwargs.get('y_grid', True)
    ratio = kwargs.get('ratio', False)

    if x_grid:
        sp.yaxis.grid(True, c=(0.9, 0.9, 0.9))
    if y_grid:
        sp.xaxis.grid(True, c=(0.9, 0.9, 0.9))

    lines = sp.get_lines()
    for line in lines:
        z_value = line.get_zorder()
        line.set_zorder(z_value + 100)
    tools.clean_chart(sp)
    sp.tick_params(axis="both", which="both", bottom=True, top=False,
                   labelbottom=True, left=True, right=False, labelleft=True)
    xlim = sp.get_xlim()
    ylim = sp.get_ylim()
    # set to xy origin:
    sp.set_xlim([0, xlim[1]])
    sp.set_ylim([0, ylim[1]])

    if ratio:
        xlim = sp.get_xlim()
        sp.plot(xlim, [1, 1], c=cbox('dark gray'), lw=0.7, zorder=50)


def save_plot_state(sub_plot, name):
    from pathlib import Path
    home = str(Path.home())
    with open(home + '/esfp_files/%s.pkl' % name, 'wb') as fid:
        pickle.dump(sub_plot, fid)


def load_plot_state(name):
    from pathlib import Path
    home = str(Path.home())
    with open(home + '/esfp_files/%s.pkl' % name, 'rb') as fid:
        ax = pickle.load(fid)
    return ax