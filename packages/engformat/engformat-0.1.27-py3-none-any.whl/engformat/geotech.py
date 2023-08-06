

def add_gwl_symbol(subplot, x_rel, y_actual):
    xlims = subplot.get_xlim()
    subplot.text(xlims[0] + (xlims[1] - xlims[0]) * x_rel, y_actual, '$\\nabla$')
