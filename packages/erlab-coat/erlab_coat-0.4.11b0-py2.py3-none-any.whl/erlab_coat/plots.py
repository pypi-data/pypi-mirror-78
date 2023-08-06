__email__ = ["shayan@cs.ucla.edu"]
__credit__ = ["ER Lab - UCLA"]

import pandas
import numpy
import matplotlib.pyplot as plt
import os
from copy import deepcopy
from plotnine import *
from plotnine.data import *
from erlab_coat.meta import *
from typing import Tuple, Union, Dict, List
from plotnine.animation import PlotnineAnimation
import plotnine
import random


def get_random_colors(n: int) -> List[Tuple[int, int, int]]:
    """
    The :func:`get_random_colors` will return a list of random colors.
    The main use of this function in this project is to assign different colors
    to different curves.

    Parameters
    ----------
    n: `int`, required
        The number of colors to be generated

    Returns
    -----------
    The output is an instance of `List[Tuple[int, int, int]]` which includes the RGB tuples of these colors.
    """
    ret = []
    r = int(random.random() * 256)
    g = int(random.random() * 256)
    b = int(random.random() * 256)
    step = 256 / n
    for i in range(n):
        r += step
        g += step
        b += step
        r = int(r) % 256
        g = int(g) % 256
        b = int(b) % 256
        ret.append((r, g, b))
    return ret


def rgb_to_hex(rgb: Tuple[int, int, int]) -> str:
    """
    This method helps with converting the rgb tuple to hex string usable in plotnine.

    Parameters
    ----------
    rgb: `Tuple[int,int,int]`, required
        The RGB tuple

    Returns
    ----------
    The `str` value usable in plotnine colors.
    """
    out = '%02x%02x%02x' % rgb
    return '#' + out.upper()


def plot_2d_infoplot(
        df: pandas.DataFrame,
        x: Tuple[str, str],
        y: Tuple[str, str],
        label: str,
        color: Tuple[str, str] = None,
        pointsize: Union[int, Tuple[str, str]] = None,
        animate_on_column: str = None,
        animate_title_prepend: str = 'Timestep value',
        label_size: int = 0,
        figure_size: int = 15,
        plot_margin: float = 0.1,
        text_element_size: int = 8,
        aspect_ratio: float = 1.0,
        subplots_adjust: Dict[str, float] = {'right': 0.85},
        xlim: Tuple[float, float] = None,
        ylim: Tuple[float, float] = None,
        color_lim: Tuple[float, float] = None,
        size_lim: Tuple[float, float] = None,
        low_color: str = '#FF0000',
        high_color: str = '#00FF00',
        colorbar_width: int = 10,
        colorbar_height: int = 100,
        color_nbin: int = 8,
        smooth_line: bool = False,
        smooth_line_color: str = 'orange',
        smooth_line_size: float = 2

) -> Union[plotnine.ggplot, plotnine.animation.PlotnineAnimation]:
    """
    The :func:`plot_2d_infoplot` is one of the most important coat methods, which is mainly responsible for
    generating the plots and forming the animations and returning them for further operations.

    Parameters
    ----------
    df: `pandas.DataFrame`, required
        The dataframe to be used in the plotter. Note that making any further preprocessing, aggregating, etc. is
        the caller's responsibility.

    x: `Tuple[str, str]`, required
        The first element is the name of the corresponding column in the dataframe, and
        the second is the label that the caller wants to observe in the actual plots / animations for it.

    y: `Tuple[str, str]`, required
        The first element is the name of the corresponding column in the dataframe, and
        the second is the label that the caller wants to observe in the actual plots / animations for it.

    label: `str`, required
        The label which is the main clustering criteria in this case. It should be a column in the dataframe.
        # TODO: do the sanity checks

    color: `Tuple[str, str]`, optional (default=None)
        The color variable, if there is any.

    pointsize: `Union[int, Tuple[str, str]]`, optional (default=None)
        The point size variable (a column in the dataframe) or an integer which is a fixed size.

    animate_on_column: `str`, optional (default=None)
        If a value is provided, the main focus of this function will be on plotting

    label_size: `int`, optional (default=0)
        If this value is something greater than 0, instead of points we will observe
        the "labels" in the plot. This is useful for example if one wants to see the regions.

    figure_size: `int`, optional (default=15)
        The figure size which will be used in plots.

    plot_margin: `float`, optional (default=0.1)
        Plot setting

    text_element_size: `int`, optional (default=8)
        Plot setting
    aspect_ratio: `float`, optional (default=1.0)
        Plot setting

    subplots_adjust: `Dict[str, float]`, optional (default={'right': 0.85})
        Plot setting mainly useful for generating the animation

    xlim: `Tuple[float, float]`, optional (default=None)
        Limits for the final plots/animations

    ylim: `Tuple[float, float]`, optional (default=None)
        Limits for the final plots/animations

    color_lim: `Tuple[float, float]`, optional (default=None)
        Limits for the final plots/animations

    size_lim: `Tuple[float, float]`, optional (default=None)
        Limits for the final plots/animations

    low_color: `str`, optional (default='#FF0000')
        If there is a color variable, this parameter can be used to set the color boundaries.

    high_color: `str`, optional (default='#00FF00')
        If there is a color variable, this parameter can be used to set the color boundaries.

    colorbar_width: `int`, optional (default=10)
        If there is a color variable, this parameter can be used to set the color guide setting.

    colorbar_height: `int`, optional (default=100)
        If there is a color variable, this parameter can be used to set the color guide setting.

    color_nbin: `int`, optional (default=8)
        If there is a color variable, this parameter can be used to set the color guide setting.

    smooth_line: `bool`, optional (default=False)
        If there is a color variable, this parameter can be used to set the color guide setting.

    smooth_line_color: `str`, optional (default='orange')
        If there is a color variable, this parameter can be used to set the color guide setting.

    smooth_line_size: `float`, optional (default=2)
        If there is a color variable, this parameter can be used to set the color guide setting.

    Returns
    ----------
    The output of this function is of type `Union[plotnine.ggplot.ggplot, plotnine.animation.PlotnineAnimation]` which
    is either a ggplot object (plotnine) or a plotnine animation (the same as matplotlib animation inherited).
    """
    # making sure to copy the dataframe and not use it by reference
    df = df.copy()

    # getting teh values
    x_var, x_label = x
    y_var, y_label = y
    if color is not None:
        color_var, color_label = color
        df[color_label] = df[color_var].copy()

    if pointsize is not None:
        if not type(pointsize) == int:
            size_var, size_label = pointsize
            df[size_label] = df[size_var].copy()

    df[x_label] = df[x_var].copy()
    df[y_label] = df[y_var].copy()

    if xlim is None:
        xlim = (
            float(df[x_var].min()), float(df[x_var].max())
        )

    if ylim is None:
        ylim = (
            float(df[y_var].min()), float(df[y_var].max())
        )

    if size_lim is None:
        if pointsize is not None:
            size_lim = (
                float(df[size_var].min()), float(df[size_var].max())
            )

    if color_lim is None:
        if color is not None:
            color_lim = (
                float(df[color_var].min()), float(df[color_var].max())
            )

    df.dropna(inplace=True)

    if animate_on_column is None:

        if (color is not None):
            p9aes = aes(
                x=x_var,
                y=y_var,
                color=color_label,
                label=label
            )
        else:
            p9aes = aes(
                x=x_var,
                y=y_var,
                label=label
            )
        # return a single plot
        single_plot = ggplot(
            df,
            p9aes
        )

        if color is not None:
            single_plot += guides(
                color=guide_colorbar(
                    barwidth=colorbar_width,
                    barheight=colorbar_height,
                    nbin=color_nbin,
                    direction='vertical',
                    ticks=True
                )
            )
            single_plot += scale_color_gradient(
                low=low_color,
                high=high_color,
                limits=(color_lim[0], color_lim[1]))

        single_plot += theme(
            subplots_adjust={'right': 0.85},
            aspect_ratio=1,
            legend_text=element_text(size=text_element_size),
            text=element_text(size=text_element_size),
            plot_margin=plot_margin,
            figure_size=(figure_size, figure_size))

        single_plot += xlab(x_label) + ylab(y_label)

        if pointsize is not None:
            if not type(pointsize) == int:
                single_plot += lims(
                    x=(xlim[0], xlim[1]), y=(ylim[0], ylim[1]), size=(size_lim[0], size_lim[1])
                )
        else:
            single_plot += lims(
                x=(xlim[0], xlim[1]), y=(ylim[0], ylim[1])
            )

        if label_size > 0:
            single_plot += geom_label(size=label_size)
        else:
            if type(pointsize) == int:
                single_plot += geom_point(size=pointsize)
            elif type(pointsize) == tuple:
                single_plot += geom_point(aes(size=size_label))
            elif pointsize is None:
                single_plot += geom_point(size=5.0)

        if smooth_line:
            if df.shape[0] > 5:
                single_plot += geom_smooth(se=False, method="loess", color=smooth_line_color, size=smooth_line_size)

        return single_plot
    else:
        timeseries_values = sorted([int(e) for e in df[animate_on_column].unique().tolist() if not pandas.isna(e)])
        plots = []
        for timeseries_value in timeseries_values:
            df_tmp = df[df[animate_on_column] == timeseries_value].copy()
            if df_tmp.shape[0] < 5:
                continue

            if (color is not None):
                p9aes = aes(
                    x=x_var,
                    y=y_var,
                    color=color_var,
                    label=label
                )
            else:
                p9aes = aes(
                    x=x_var,
                    y=y_var,
                    label=label
                )
            # return a single plot
            single_plot = ggplot(
                df_tmp,
                p9aes
            )

            if color is not None:
                single_plot += guides(
                    color=guide_colorbar(
                        barwidth=colorbar_width,
                        barheight=colorbar_height,
                        nbin=color_nbin,
                        direction='vertical',
                        ticks=True
                    )
                )
                single_plot += scale_color_gradient(
                    low=low_color,
                    high=high_color,
                    limits=(color_lim[0], color_lim[1]))

            single_plot += theme(
                subplots_adjust=subplots_adjust,
                aspect_ratio=aspect_ratio,
                legend_text=element_text(size=text_element_size),
                text=element_text(size=text_element_size),
                plot_margin=plot_margin,
                figure_size=(figure_size, figure_size))

            single_plot += xlab(x_label) + ylab(y_label)

            if pointsize is not None:
                if not type(pointsize) == int:
                    single_plot += lims(
                        x=(xlim[0], xlim[1]), y=(ylim[0], ylim[1]), size=(size_lim[0], size_lim[1])
                    )
            else:
                single_plot += lims(
                    x=(xlim[0], xlim[1]), y=(ylim[0], ylim[1])
                )

            if label_size > 0:
                single_plot += geom_label(size=label_size)
            else:
                if type(pointsize) == int:
                    single_plot += geom_point(size=pointsize)
                elif type(pointsize) == tuple:
                    single_plot += geom_point(aes(size=size_label))
                elif pointsize is None:
                    single_plot += geom_point(size=5.0)

            if smooth_line:
                if df_tmp[x_var].unique().shape[0] > 10:
                    single_plot += geom_smooth(se=False, method="loess", color=smooth_line_color, size=smooth_line_size)

            single_plot += annotate('text', x=xlim[1] / 2.0, y=ylim[1],
                                    label="{}: {}".format(animate_title_prepend, timeseries_value))

            plots.append(single_plot)

        animation = PlotnineAnimation(tuple(plots), interval=100, repeat_delay=5, blit=True)
        return animation


def plot_2d_infoplot_on_timeseries_temporal_effect(
        df: pandas.DataFrame,
        x: Tuple[str, str],
        y: Tuple[str, str],
        color: Tuple[str, str] = None,
        figure_size: int = 15,
        plot_margin: float = 0.1,
        text_element_size: int = 8,
        aspect_ratio: float = 1.0,
        subplots_adjust: Dict[str, float] = {'right': 0.85},
        xlim: Tuple[float, float] = None,
        ylim: Tuple[float, float] = None,
        animate: bool = False

) -> Union[plotnine.ggplot, plotnine.animation.PlotnineAnimation]:
    """
    The :func:`plot_2d_infoplot_on_timeseries_temporal_effect` is the main functionalities of plotting summarized
    for temporal effect monitoring both in terms of animation generation and static plot.

    Parameters
    ----------
    df: `pandas.DataFrame`, required
        The dataframe to be used in the plotter. Note that making any further preprocessing, aggregating, etc. is
        the caller's responsibility.

    x: `Tuple[str, str]`, required
        The first element is the name of the corresponding column in the dataframe, and
        the second is the label that the caller wants to observe in the actual plots / animations for it.

    y: `Tuple[str, str]`, required
        The first element is the name of the corresponding column in the dataframe, and
        the second is the label that the caller wants to observe in the actual plots / animations for it.

    label: `str`, required
        The label which is the main clustering criteria in this case. It should be a column in the dataframe.
        # TODO: do the sanity checks

    color: `Tuple[str, str]`, optional (default=None)
        The color variable, if there is any.

    figure_size: `int`, optional (default=15)
        The figure size which will be used in plots.

    plot_margin: `float`, optional (default=0.1)
        Plot setting

    text_element_size: `int`, optional (default=8)
        Plot setting
    aspect_ratio: `float`, optional (default=1.0)
        Plot setting

    subplots_adjust: `Dict[str, float]`, optional (default={'right': 0.85})
        Plot setting mainly useful for generating the animation

    xlim: `Tuple[float, float]`, optional (default=None)
        Limits for the final plots/animations

    ylim: `Tuple[float, float]`, optional (default=None)
        Limits for the final plots/animations



    Returns
    ----------
    The output of this function is of type `Union[plotnine.ggplot.ggplot, plotnine.animation.PlotnineAnimation]` which
    is either a ggplot object (plotnine) or a plotnine animation (the same as matplotlib animation inherited).
    """
    # making sure to copy the dataframe and not use it by reference
    df = df.copy()

    # getting teh values
    x_var, x_label = x
    y_var, y_label = y

    if color is not None:
        color_var, color_label = color
        df[color_label] = df[color_var].copy()

    df[x_label] = df[x_var].copy()
    df[y_label] = df[y_var].copy()

    if xlim is None:
        xlim = (
            float(df[x_var].min()), float(df[x_var].max())
        )

    if ylim is None:
        ylim = (
            float(df[y_var].min()), float(df[y_var].max())
        )

    df.dropna(inplace=True)

    if not animate:
        if (color is not None):
            p9aes = aes(
                x=x_var,
                y=y_var,
                color=color_var
            )
        else:
            p9aes = aes(
                x=x_var,
                y=y_var
            )
        # return a single plot
        single_plot = ggplot(
            df,
            p9aes
        )

        single_plot += theme(
            subplots_adjust={'right': 0.85},
            aspect_ratio=1,
            legend_text=element_text(size=text_element_size),
            text=element_text(size=text_element_size),
            plot_margin=plot_margin,
            figure_size=(figure_size, figure_size))

        single_plot += xlab(x_label) + ylab(y_label)

        single_plot += lims(
            x=(xlim[0], xlim[1]), y=(ylim[0], ylim[1])
        )

        single_plot += geom_point(size=5.0)
        single_plot += geom_line(size=2.0)

        return single_plot
    else:
        plots = []

        timeseries_values = sorted([int(e) for e in df[x_var].unique().tolist() if not pandas.isna(e)])

        random_colors = [rgb_to_hex(e) for e in get_random_colors(len(df[color_var].unique().tolist().copy()))]

        for timeseries_value in timeseries_values:
            tmp_df = df[df[x_var] <= timeseries_value].copy()
            check_df = tmp_df[tmp_df[x_var] == timeseries_value]
            if not len(check_df[color_var].unique().tolist()) == len(random_colors):
                df = df[df[x_var] > timeseries_value].copy()
                continue
            if (color is not None):
                p9aes = aes(
                    x=x_var,
                    y=y_var,
                    color=color_var
                )
            else:
                p9aes = aes(
                    x=x_var,
                    y=y_var
                )
            # return a single plot
            single_plot = ggplot(
                tmp_df,
                p9aes
            )

            single_plot += theme(
                subplots_adjust=subplots_adjust,
                aspect_ratio=aspect_ratio,
                legend_text=element_text(size=text_element_size),
                text=element_text(size=text_element_size),
                plot_margin=plot_margin,
                figure_size=(figure_size, figure_size))

            single_plot += xlab(x_label) + ylab(y_label)

            single_plot += lims(
                x=(xlim[0], xlim[1]), y=(ylim[0], ylim[1])
            )

            single_plot += geom_point(size=5.0)
            single_plot += geom_line(size=2.0)
            single_plot += scale_color_manual(values=random_colors)

            plots.append(single_plot)
        animation = PlotnineAnimation(tuple(plots), interval=100, repeat_delay=5, blit=True)
        return animation
