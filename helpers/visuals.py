import matplotlib.pyplot as plt


def strike_rate_line_generator(strike_rate, max_x, max_y):
    x = 0
    y = 0
    x_points = []
    y_points = []

    while x <= max_x and y <= max_y:
        x_points.append(round(x, 2))
        y_points.append(round(y, 2))
        x = x + 1
        y = y + 1 * (strike_rate / 100)

    return x_points, y_points


def plot_strike_rate_line(strike_rate, x_lim, y_lim, ax=None, **kwargs):
    sr_points = strike_rate_line_generator(strike_rate, x_lim, y_lim)
    ax = ax or plt.gca()

    label_x = max(sr_points[0])
    label_y = max(sr_points[1])
    h_align = "left"
    v_align = "center"

    if label_x >= label_y:
        label_x = x_lim + 2
    else:
        label_y = y_lim + 2
        h_align = "center"
        v_align = "baseline"

    if 'c' in kwargs:
        text_color = kwargs.get('c')
    else:
        text_color = '#d1ccc0'

    ax.text(label_x,
            label_y,
            f'{round(strike_rate, 2)} SR',
            fontsize=9,
            horizontalalignment=h_align,
            verticalalignment=v_align,
            color=text_color)

    return ax.plot(sr_points[0], sr_points[1], **kwargs)
