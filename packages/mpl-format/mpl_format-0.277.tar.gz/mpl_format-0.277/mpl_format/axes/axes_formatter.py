from pathlib import Path
from typing import Optional, Union, List, Tuple, Iterable

import matplotlib.pyplot as plt
from matplotlib.axes import Axes
from matplotlib.collections import PathCollection
from matplotlib.font_manager import FontProperties
from matplotlib.patches import Rectangle
from pandas import DataFrame

from compound_types.arrays import ArrayLike
from compound_types.built_ins import FloatOrFloatIterable, StrOrStrIterable, \
    DictOrDictIterable
from mpl_format.axes.axis_formatter import AxisFormatter
from mpl_format.axes.axis_utils import new_axes
from mpl_format.compound_types import FontSize, Color, LegendLocation, \
    StringMapper
from mpl_format.io_utils import save_plot
from mpl_format.legend.legend_formatter import LegendFormatter
from mpl_format.patches.patch_list_formatter import PatchListFormatter
from mpl_format.text.text_formatter import TextFormatter
from mpl_format.text.text_utils import wrap_text


class AxesFormatter(object):

    def __init__(self, axes: Optional[Axes] = None,
                 width: Optional[int] = None, height: Optional[int] = None,
                 constrained_layout: bool = False):
        """
        Create a new AxesFormatter

        :param axes: The matplotlib Axes instance to wrap.
        :param width: Width of new Axes, if none are given.
        :param height: Height of new Axes, if none are given.
        :param constrained_layout: Option for constrained_layout of new Axes.
        """
        if axes is None:
            self._axes: Axes = new_axes(
                width=width, height=height,
                constrained_layout=constrained_layout
            )
        else:
            self._axes: Axes = axes
        self._x_axis: AxisFormatter = AxisFormatter(self._axes.xaxis)
        self._y_axis: AxisFormatter = AxisFormatter(self._axes.yaxis)
        self._title: TextFormatter = TextFormatter(self._axes.title)
        legend = self._axes.get_legend()
        if legend is None:
            self._legend = None
        else:
            self._legend = LegendFormatter(legend)

    # region properties

    @property
    def axes(self) -> Axes:
        """
        Return the wrapped Axes instance.
        """
        return self._axes

    @property
    def x_axis(self) -> AxisFormatter:
        """
        Return an AxisFormatter for the x-axis of the wrapped Axes.
        """
        return self._x_axis

    @property
    def y_axis(self) -> AxisFormatter:
        """
        Return an AxisFormatter for the y-axis of the wrapped Axes.
        """
        return self._y_axis

    @property
    def legend(self) -> LegendFormatter:
        """
        Return a LegendFormatter for the legend of the wrapped Axes,
        if there is one.
        """
        return self._legend

    @property
    def title(self) -> TextFormatter:
        return self._title

    # endregion

    # region set text

    def set_title_text(self, text: str) -> 'AxesFormatter':
        """
        Set the text of the Axes title.

        :param text: The text to use for the Axes title.
        """
        self.title.set_text(text)
        return self

    def map_title_text(
            self, mapping: StringMapper
    ) -> 'AxesFormatter':
        """
        Map the label text for the title using a dictionary or function.

        :param mapping: Dictionary or a function mapping old text to new text.
        """
        self.title.map(mapping=mapping)
        return self

    def set_x_label_text(self, text: str) -> 'AxesFormatter':
        """
        Set the text for the x-axis label.

        :param text: The text to use for the Axis label.
        """
        self.x_axis.set_label_text(text)
        return self

    def set_y_label_text(self, text: str) -> 'AxesFormatter':
        """
        Set the text for the y-axis label.

        :param text: The text to use for the Axis label.
        """
        self.y_axis.set_label_text(text)
        return self

    def set_text(self, title: Optional[str] = None,
                 x_label: Optional[str] = None,
                 y_label: Optional[str] = None) -> 'AxesFormatter':
        """
        Set text properties for elements of the Axes.

        :param title: Text for the title.
        :param x_label: Text for the x-axis label.
        :param y_label: Text for the y-axis label.
        """
        if title is not None:
            self.set_title_text(title)
        if x_label is not None:
            self.x_axis.set_label_text(x_label)
        if y_label is not None:
            self.y_axis.set_label_text(y_label)
        return self

    # endregion

    # region wrap text

    def wrap_title(self, max_width: int) -> 'AxesFormatter':
        """
        Wrap the text for the title if it exceeds a given width of characters.

        :param max_width: The maximum character width per line.
        """
        self.set_title_text(wrap_text(self.title.text, max_width=max_width))
        return self

    def wrap_x_label(self, max_width: int) -> 'AxesFormatter':
        """
        Wrap the text for the x-axis label if it exceeds a given width of
        characters.

        :param max_width: The maximum character width per line.
        """
        self.x_axis.wrap_label(max_width=max_width)
        return self

    def wrap_y_label(self, max_width: int) -> 'AxesFormatter':
        """
        Wrap the text for the y-axis label if it exceeds a given width of
        characters.

        :param max_width: The maximum character width per line.
        """
        self.y_axis.wrap_label(max_width=max_width)
        return self

    def wrap_x_tick_labels(self, max_width: int) -> 'AxesFormatter':
        """
        Wrap the text for each tick label on the x-axis with new lines if it
        exceeds a given width of characters.

        :param max_width: The maximum character width per line.
        """
        self.x_axis.wrap_tick_labels(max_width=max_width)
        return self

    def wrap_y_tick_labels(self, max_width: int) -> 'AxesFormatter':
        """
        Wrap the text for each tick label on the y-axes with new lines if it
        exceeds a given width of characters.

        :param max_width: The maximum character width per line.
        """
        self.y_axis.wrap_tick_labels(max_width=max_width)
        return self

    def wrap_tick_labels(self, max_width: int) -> 'AxesFormatter':
        """
        Wrap the text for each tick label on each axis with new lines if it
        exceeds a given width of characters.

        :param max_width: The maximum character width per line.
        """
        self.wrap_x_tick_labels(max_width=max_width)
        self.wrap_y_tick_labels(max_width=max_width)
        return self

    # endregion

    # region set font sizes

    def set_title_size(self, font_size: FontSize) -> 'AxesFormatter':
        """
        Set the font size for the title of the wrapped Axes.

        :param font_size: Size of the font in points, or size name.
        """
        self.title.set_size(font_size)
        return self

    def set_x_label_size(self, font_size: FontSize) -> 'AxesFormatter':
        """
        Set the font size for the x-axis label.

        :param font_size: Size of the font in points, or size name.
        """
        self.x_axis.set_label_size(font_size)
        return self

    def set_y_label_size(self, font_size: FontSize) -> 'AxesFormatter':
        """
        Set the font size for the x-axis label.

        :param font_size: Size of the font in points, or size name.
        """
        self.y_axis.set_label_size(font_size)
        return self

    def set_axis_label_sizes(self, font_size: FontSize) -> 'AxesFormatter':
        """
        Set the font size for the axis labels.

        :param font_size: Size of the font in points, or size name.
        """
        self.set_x_label_size(font_size)
        self.set_y_label_size(font_size)
        return self

    def set_x_tick_label_size(self, font_size: FontSize) -> 'AxesFormatter':
        """
        Set the font size for the x-axis tick labels.

        :param font_size: Size of the font in points, or size name.
        """
        self.x_axis.set_tick_label_size(font_size)
        return self

    def set_y_tick_label_size(self, font_size: FontSize) -> 'AxesFormatter':
        """
        Set the font size for the y-axis tick labels.

        :param font_size: Size of the font in points, or size name.
        """
        self.y_axis.set_tick_label_size(font_size)
        return self

    def set_tick_label_sizes(self, font_size: FontSize) -> 'AxesFormatter':
        """
        Set the font size for the tick labels of the wrapped Axes.

        :param font_size: Size of the font in points, or size name.
        """
        self.set_x_tick_label_size(font_size)
        self.set_y_tick_label_size(font_size)
        return self

    def set_font_sizes(
            self,
            title: Optional[int] = None,
            axis_labels: Optional[int] = None,
            x_axis_label: Optional[int] = None,
            y_axis_label: Optional[int] = None,
            tick_labels: Optional[int] = None,
            x_tick_labels: Optional[int] = None,
            y_tick_labels: Optional[int] = None,
            legend: Optional[int] = None,
            figure_title: Optional[int] = None
    ) -> 'AxesFormatter':
        """
        Set font sizes for different axes elements.
        """
        ax = self._axes
        if title is not None:
            self.set_title_size(title)
        if axis_labels is not None:
            self.set_axis_label_sizes(axis_labels)
        if x_axis_label is not None:
            self.set_x_label_size(x_axis_label)
        if y_axis_label is not None:
            self.set_y_label_size(y_axis_label)
        if tick_labels is not None:
            self.set_tick_label_sizes(tick_labels)
        if x_tick_labels is not None:
            self.set_x_tick_label_size(x_tick_labels)
        if y_tick_labels is not None:
            self.set_y_label_size(y_tick_labels)
        if legend is not None:
            ax.legend(fontsize=legend)
        if figure_title is not None:
            ax.figure.suptitle(ax.get_title(), fontsize=figure_title)

        return self

    # endregion

    # region map labels

    def map_x_axis_label(
            self, mapping: StringMapper
    ) -> 'AxesFormatter':
        """
        Map the label text for the x-axis using a dictionary or function.

        :param mapping: Dictionary or a function mapping old text to new text.
        """
        self.x_axis.map_label_text(mapping)
        return self

    def map_y_axis_label(
            self, mapping: StringMapper
    ) -> 'AxesFormatter':
        """
        Map the label text for the y-axis using a dictionary or function.

        :param mapping: Dictionary or a function mapping old text to new text.
        """
        self.y_axis.map_label_text(mapping)
        return self

    def map_axis_labels(
            self, mapping: StringMapper
    ) -> 'AxesFormatter':
        """
        Map the label text for the x and y axes using a dictionary or function.

        :param mapping: Dictionary or a function mapping old text to new text.
        """
        self.map_x_axis_label(mapping)
        self.map_y_axis_label(mapping)
        return self

    def map_x_tick_labels(
            self, mapping: StringMapper
    ) -> 'AxesFormatter':
        """
        Map the tick label text for the x-axis using a dictionary or function.

        :param mapping: Dictionary or a function mapping old text to new text.
        """
        self.x_axis.map_tick_label_text(mapping)
        return self

    def map_y_tick_labels(
            self, mapping: StringMapper
    ) -> 'AxesFormatter':
        """
        Map the tick label text for the y-axis using a dictionary or function.

        :param mapping: Dictionary or a function mapping old text to new text.
        """
        self.y_axis.map_tick_label_text(mapping)
        return self

    def map_tick_labels(
            self, mapping: StringMapper
    ) -> 'AxesFormatter':
        """
        Map the tick label text using a dictionary or function.

        :param mapping: Dictionary or a function mapping old text to new text.
        """
        self.map_x_tick_labels(mapping)
        self.map_y_tick_labels(mapping)
        return self

    # endregion

    # region remove

    def remove_title(self) -> 'AxesFormatter':
        """
        Remove the title from the Axes.
        """
        self.set_title_text('')
        return self

    def remove_legend(self) -> 'AxesFormatter':
        """
        Remove the legend from the Axes.
        """
        legend = self._axes.get_legend()
        if legend is not None:
            legend.remove()
            self._legend = None
        return self

    def remove_x_ticks(self) -> 'AxesFormatter':
        """
        Remove x-ticks from the Axes.
        """
        self._axes.set_xticks([])
        return self

    def remove_y_ticks(self) -> 'AxesFormatter':
        """
        Remove y-ticks from the Axes.
        """
        self._axes.set_yticks([])
        return self

    def remove_axes_ticks(self) -> 'AxesFormatter':
        """
        Remove x- and y- ticks from the Axes.
        """
        self.remove_x_ticks()
        self.remove_y_ticks()
        return self

    def remove_x_label(self) -> 'AxesFormatter':
        """
        Remove the label from the x-axis.
        """
        self.x_axis.remove_label()
        return self

    def remove_y_label(self) -> 'AxesFormatter':
        """
        Remove the label from the y-axis.
        """
        self.y_axis.remove_label()
        return self

    def remove_axes_labels(self) -> 'AxesFormatter':
        """
        Remove the labels from the x- and y- axes.
        """
        self.remove_x_label()
        self.remove_y_label()
        return self

    # endregion

    # region rotation

    def rotate_x_label(self,
                       rotation: int,
                       how: str = 'absolute') -> 'AxesFormatter':
        """
        Set the rotation of the x-axis label.

        :param rotation: The rotation value to set in degrees.
        :param how: 'absolute' or 'relative'
        """
        self.x_axis.rotate_label(rotation, how)
        return self

    def rotate_y_label(self,
                       rotation: int,
                       how: str = 'absolute') -> 'AxesFormatter':
        """
        Set the rotation of the x-axis label.

        :param rotation: The rotation value to set in degrees.
        :param how: 'absolute' or 'relative'
        """
        self.y_axis.rotate_label(rotation, how)
        return self

    def rotate_x_tick_labels(self,
                             rotation: int,
                             how: str = 'absolute') -> 'AxesFormatter':
        """
        Set the rotation of the x-axis tick labels.

        :param rotation: The rotation value to set in degrees.
        :param how: 'absolute' or 'relative'
        """
        self.x_axis.rotate_tick_labels(rotation=rotation, how=how)
        return self

    def rotate_y_tick_labels(self,
                             rotation: int,
                             how: str = 'absolute') -> 'AxesFormatter':
        """
        Set the rotation of the y-axis tick labels.

        :param rotation: The rotation value to set in degrees.
        :param how: 'absolute' or 'relative'
        """
        self.y_axis.rotate_tick_labels(rotation=rotation, how=how)
        return self

    # endregion

    # region spans

    def add_h_line(self, y: Union[float, str] = 0,
                   x_min: Union[float, str] = 0,
                   x_max: Union[float, str] = 1,
                   color: Optional[Color] = None,
                   alpha: Optional[float] = None,
                   line_style: Optional[str] = None,
                   line_width: Optional[float] = None,
                   marker_edge_color: Optional[Color] = None,
                   marker_edge_width: Optional[Color] = None,
                   marker_face_color: Optional[Color] = None,
                   marker_size: Optional[float] = None) -> 'AxesFormatter':
        """
        Add a horizontal line to the plot.

        :param y: y position in data coordinates of the horizontal line
        :param x_min: Between 0 and 1, 0 being the far left of the plot,
                      1 the far right of the plot
        :param x_max: Between 0 and 1, 0 being the far left of the plot,
                      1 the far right of the plot
        :param color: Color of the line
        :param alpha: Opacity of the line
        :param line_style: One of {'-', '--', '-.', ':', ''}
        :param line_width: Width of the line
        :param marker_edge_color: Color for the edges of the line markers
        :param marker_edge_width: Width for the edges of the line markers
        :param marker_face_color: Color for the markers
        :param marker_size: Size of the markers.
        """
        kwargs = {}
        for arg, mpl_arg in zip(
            [color, line_style, line_width,
             marker_edge_color, marker_edge_width,
             marker_face_color, marker_size,
             alpha],
            ['c', 'ls', 'lw', 'mec', 'mew', 'mfc', 'ms', 'alpha']
        ):
            if arg is not None:
                kwargs[mpl_arg] = arg

        self._axes.axhline(
            y=y, xmin=x_min, xmax=x_max,
            **kwargs
        )
        return self

    def add_v_line(self, x: Union[float, str] = 0,
                   y_min: Union[float, str] = 0,
                   y_max: Union[float, str] = 1,
                   color: Optional[Color] = None, alpha: Optional[float] = None,
                   line_style: Optional[str] = None,
                   line_width: Optional[float] = None,
                   marker_edge_color: Optional[Color] = None,
                   marker_edge_width: Optional[Color] = None,
                   marker_face_color: Optional[Color] = None,
                   marker_size: Optional[float] = None) -> 'AxesFormatter':
        """
        Add a vertical line to the plot.

        :param x: x position in data coordinates of the vertical line
        :param y_min: Should be between 0 and 1, with 0 being the bottom of the
                      plot, and 1 the top of the plot
        :param y_max: Should be between 0 and 1, with 0 being the bottom of the
                      plot, and 1 the top of the plot
        :param color: Color of the line
        :param alpha: Opacity of the line
        :param line_style: One of {'-', '--', '-.', ':', ''}
        :param line_width: Width of the line
        :param marker_edge_color: Color for the edges of the line markers
        :param marker_edge_width: Width for the edges of the line markers
        :param marker_face_color: Color for the markers
        :param marker_size: Size of the markers.
        """
        kwargs = {}
        for arg, mpl_arg in zip(
            [color, line_style, line_width, marker_edge_color,
             marker_edge_width, marker_face_color, marker_size, alpha],
            ['c', 'ls', 'lw', 'mec', 'mew', 'mfc', 'ms', 'alpha']
        ):
            if arg is not None:
                kwargs[mpl_arg] = arg

        self._axes.axvline(
            x=x, ymin=y_min, ymax=y_max,
            **kwargs
        )
        return self

    def add_h_lines(self, y: FloatOrFloatIterable,
                    x_min: FloatOrFloatIterable,
                    x_max: FloatOrFloatIterable,
                    colors='k', line_styles: str = 'solid',
                    label: Optional[str] = '') -> 'AxesFormatter':
        """
        Plot horizontal lines at each y from x_min to x_max.

        :param y: x-indexes where to plot the lines.
        :param x_min: Beginning of each or all lines.
        :param x_max: End of each or all lines.
        :param colors: Line colors.
        :param line_styles: One of {'solid', 'dashed', 'dashdot', 'dotted'}
        :param label: Label.
        """
        self._axes.hlines(y=y, xmin=x_min, xmax=x_max,
                          colors=colors, linestyles=line_styles,
                          label=label)
        return self

    def add_v_lines(self, x: FloatOrFloatIterable,
                    y_min: FloatOrFloatIterable,
                    y_max: FloatOrFloatIterable,
                    colors='k', line_styles: str = 'solid',
                    label: Optional[str] = '') -> 'AxesFormatter':
        """
        Plot vertical lines at each x from y_min to y_max.

        :param x: x-indexes where to plot the lines.
        :param y_min: Beginning of each or all lines.
        :param y_max: End of each or all lines.
        :param colors: Line colors.
        :param line_styles: One of {'solid', 'dashed', 'dashdot', 'dotted'}
        :param label: Label.
        """
        self._axes.vlines(x=x, ymin=y_min, ymax=y_max,
                          colors=colors, linestyles=line_styles,
                          label=label)
        return self

    def fill_between(self, x: Union[ArrayLike, str],
                     y1: Union[float, ArrayLike, str],
                     y2: Union[float, ArrayLike, str],
                     data: Optional[DataFrame] = None,
                     where: Optional[ArrayLike] = None,
                     interpolate: bool = False,
                     step: Optional[str] = None,
                     color: Optional[Color] = None,
                     alpha: Optional[float] = None,
                     line_style: Optional[str] = None,
                     line_width: Optional[float] = None,
                     edge_color: Optional[Color] = None,
                     face_color: Optional[Color] = None) -> 'AxesFormatter':
        """
        Make filled polygons between two curves.

        :param x: N-length array of, or name of column with the x data.
        :param y1: N-length array, scalar, or name of column with the y1 data.
        :param y2: N-length array, scalar, or name of column with the y2 data.
        :param data: Optional DataFrame with x, y1 and y2 columns.
        :param where: If None, default to fill between everywhere. If not None,
                      it is an N-length numpy boolean array and the fill will
                      only happen over the regions where where==True.
        :param interpolate: If True, interpolate between the two lines to find
                            the precise point of intersection. Otherwise, the
                            start and end points of the filled region will only
                            occur on explicit values in the x array.
        :param step: One of {‘pre’, ‘post’, ‘mid’}. If not None, fill with step
                     logic.
        :param color: matplotlib color arg or sequence of rgba tuples
        :param alpha: Opacity.
        :param line_style: One of {'-', '--', '-.', ':', ''}
        :param line_width: float or sequence of floats
        :param edge_color: matplotlib color spec or sequence of specs
        :param face_color: matplotlib color spec or sequence of specs
        """
        # get arrays from DataFrame
        if data is not None:
            if isinstance(x, str):
                x = data[x]
            if isinstance(y1, str):
                y1 = data[y1]
            if isinstance(y2, str):
                y2 = data[y2]
        # convert args to matplotlib names
        kwargs = {}
        for arg, mpl_arg in zip(
            [color, alpha, line_style, line_width, edge_color, face_color],
            ['color', 'alpha', 'line_style',
             'line_width', 'edge_color', 'face_color']
        ):
            if arg is not None:
                kwargs[mpl_arg] = arg
        # call matplotlib method
        self._axes.fill_between(
            x=x, y1=y1, y2=y2,
            where=where, interpolate=interpolate,
            step=step,
            **kwargs
        )
        return self

    # endregion

    # region colors

    def set_face_color(self, color: Color) -> 'AxesFormatter':

        self._axes.set_facecolor(color)
        return self

    def get_frame_color(self) -> Union[Color, List[Color]]:
        """
        Return the color of the frame if all edges are the same color,
        otherwise a list of the top, bottom, left and right colors.
        """
        colors = self.get_frame_colors()
        if len(set(colors)) == 1:
            return colors[0]
        else:
            return self.get_frame_colors()

    def set_frame_color(self, color: Color) -> 'AxesFormatter':

        for pos in ['top', 'bottom', 'left', 'right']:
            self._axes.spines[pos].set_edgecolor(color)
        return self

    def get_frame_colors(self) -> List[Color]:
        """
        Return the colors of the top, bottom, left and right edges of the Axes.
        """
        return [
            self._axes.spines[pos].get_edgecolor()
            for pos in ['top', 'bottom', 'left', 'right']
        ]

    def set_tick_color(self, color: Color) -> 'AxesFormatter':

        self.x_axis.set_tick_color(color=color)
        self.y_axis.set_tick_color(color=color)
        return self

    # endregion

    # region shapes

    @property
    def rectangles(self) -> PatchListFormatter:
        """
        Return a list of the Rectangles on the axes.
        """
        return PatchListFormatter([
            r for r in self._axes.get_children()
            if isinstance(r, Rectangle)
        ])

    def add_text(
            self, x: FloatOrFloatIterable,
            y: FloatOrFloatIterable,
            text: StrOrStrIterable,
            font_dict: Optional[DictOrDictIterable] = None,
            **kwargs
    ) -> 'AxesFormatter':
        """
        Add a single or multiple text blocks to the plot.

        :param x: x-coordinate(s) of the text.
        :param y: y-coordinate(s) of the text.
        :param text: String or iterable of text strings to add.
        :param font_dict: A dictionary to override the default text properties.
                          If font_dict is None, the defaults are determined by
                          your rc parameters.
        :param kwargs: Other miscellaneous Text parameters.
        """
        if isinstance(x, Iterable) or isinstance(y, Iterable):
            if not isinstance(x, Iterable):
                x = [x] * len(y)
            elif not isinstance(y, Iterable):
                y = [y] * len(x)
        else:
            x = [x]
            y = [y]
            if isinstance(text, str):
                text = [text] * len(x)
            if type(font_dict) in (type(None), dict):
                font_dict = [font_dict] * len(x)

        for x_i, y_i, text_i, font_dict_i in zip(x, y, text, font_dict):
            self._axes.text(
                x=x_i, y=y_i, s=text_i,
                fontdict=font_dict_i, **kwargs
            )
        return self

    # endregion

    def set_title_font_family(self, font_name: str) -> 'AxesFormatter':
        """
        Set the font family for the Axes title.

        :param font_name: Name of the font.
        """
        self.title.set_font_family(font_name)
        return self

    # region limits

    def get_x_lim(self) -> Tuple[float, float]:
        """
        Return the x-axis view limits.
        """
        return self._axes.get_xlim()

    def get_y_lim(self) -> Tuple[float, float]:
        """
        Return the y-axis view limits.
        """
        return self._axes.get_ylim()

    def set_x_lim(self, left: Optional[float] = None,
                  right: Optional[float] = None) -> 'AxesFormatter':
        """
        Set the limits of the x-axis.

        :param left: Lower limit.
        :param right: Upper limit.
        """
        self._axes.set_xlim(left=left, right=right)
        return self

    def set_y_lim(self, bottom: Optional[float] = None,
                  top: Optional[float] = None) -> 'AxesFormatter':
        """
        Set the limits of the y-axis.

        :param bottom: Lower limit.
        :param top: Upper limit.
        """
        self._axes.set_ylim(bottom=bottom, top=top)
        return self

    def get_x_min(self) -> float:
        """
        Return the x-axis lower view limit.
        """
        return self.get_x_lim()[0]

    def get_x_max(self) -> float:
        """
        Return the x-axis upper view limit.
        """
        return self.get_x_lim()[1]

    def set_x_min(self, left: float = None) -> 'AxesFormatter':
        """
        Set the x-axis lower view limit.
        """
        self.set_x_lim(left, None)
        return self

    def set_x_max(self, right: float = None) -> 'AxesFormatter':
        """
        Set the x-axis upper view limit.
        """
        self.set_x_lim(None, right)
        return self

    def get_y_min(self) -> float:
        """
        Return the y-axis lower view limit.
        """
        return self.get_y_lim()[0]

    def get_y_max(self) -> float:
        """
        Return the y-axis upper view limit.
        """
        return self.get_y_lim()[1]

    def set_y_min(self, left: float = None) -> 'AxesFormatter':
        """
        Set the y-axis lower view limit.
        """
        self.set_y_lim(left, None)
        return self

    def set_y_max(self, right: float = None) -> 'AxesFormatter':
        """
        Set the y-axis upper view limit.
        """
        self.set_y_lim(None, right)
        return self

    # endregion

    def grid(self, value: bool = True,
             which: str = 'major',
             axis: str = 'both') -> 'AxesFormatter':
        """
        Turn the grid on or off.

        :param value: True or False. Defaults to True.
        :param which: 'major', 'minor' or 'both'
        :param axis: 'x', 'y' or 'both
        """
        self._axes.grid(b=value, which=which, axis=axis)
        return self

    def set_axis_below(self,
                       value: bool = True) -> 'AxesFormatter':
        """
        Set whether axis ticks and gridlines are above or below most artists.

        :param value: True or False
        """
        self._axes.set_axisbelow(b=value)
        return self

    def save(self,
             file_path: Union[str, Path],
             file_type: str = 'png') -> 'AxesFormatter':
        """
        Save the plot to disk.

        :param file_path: The file path to save the plot object to.
        :param file_type: The type of file to save.
        """
        save_plot(plot_object=self._axes,
                  file_path=file_path,
                  file_type=file_type)
        return self

    def tight_layout(self) -> 'AxesFormatter':
        """
        Call the tight_layout method on the Axes' figure.
        """
        self._axes.figure.tight_layout()
        return self

    def invert_x_axis(self) -> 'AxesFormatter':
        """
        Invert the x-axis.
        """
        self.x_axis.invert()
        return self

    def invert_y_axis(self) -> 'AxesFormatter':
        """
        Invert the y-axis.
        """
        self.y_axis.invert()
        return self

    def add_legend(
            self,
            handles: Optional[List[PathCollection]] = None,
            labels: Optional[List[str]] = None,
            location: Optional[LegendLocation] = None,
            n_cols: Optional[int] = None,
            font_size: Optional[str] = None,
            font_properties: Optional[Union[FontProperties, dict]] = None,
            line_points: Optional[int] = None,
            scatter_points: Optional[int] = None,
            scatter_y_offsets: Optional[ArrayLike] = None,
            marker_scale: Optional[float] = None,
            frame_on: Optional[bool] = None,
            shadow: Optional[bool] = None,
            frame_alpha: Optional[float] = None,
            face_color: Optional[Color] = None,
            edge_color: Optional[Color] = None,
            mode: Optional[str] = None,
            title: Optional[str] = None,
            title_font_size: Optional[FontSize] = None,
            label_spacing: Optional[float] = None,
            handle_length: Optional[float] = None,
            handle_text_pad: Optional[float] = None,
            border_axes_pad: Optional[float] = None,
            column_spacing: Optional[float] = None
    ) -> LegendFormatter:
        """
        Add a legend to the Axes.

        :param handles: A list of Artists (lines, patches) to be added to the
                        legend.
        :param labels: A list of labels to show next to the artists. The length
                       of handles and labels should be the same. If they are
                       not, they are truncated to the smaller of both lengths.
        :param location: The legend location.
        :param n_cols: The number of columns that the legend has. Default is 1.
        :param font_size: The font size of the legend. If the value is numeric
                          the size will be the absolute font size in points.
                          String values are relative to the current default font
                          size. This argument is only used if font_properties is
                          not specified.
        :param font_properties: The font properties of the legend. If None
                                (default), the current matplotlib.rcParams will
                                be used.
        :param line_points: The number of marker points in the legend when
                            creating a legend entry for a Line2D (line).
                            Default is None, which means using
                            rcParams["legend.numpoints"] (default: 1).
        :param scatter_points: The number of marker points in the legend when
                               creating a legend entry for a PathCollection
                               (scatter plot). Default is None, which means using
                               rcParams["legend.scatterpoints"] (default: 1).
        :param scatter_y_offsets: The vertical offset (relative to the font size)
                                  for the markers created for a scatter plot
                                  legend entry. 0.0 is at the base the legend
                                  text, and 1.0 is at the top. To draw all
                                  markers at the same height, set to [0.5].
                                  Default is [0.375, 0.5, 0.3125].
        :param marker_scale: The relative size of legend markers compared with
                             the originally drawn ones. Default is None, which
                             means using rcParams["legend.markerscale"]
                             (default: 1.0).
        :param frame_on: Whether the legend should be drawn on a patch (frame).
                         Default is None, which means using
                         rcParams["legend.frameon"] (default: True).
        :param shadow: Whether to draw a shadow behind the legend. Default is
                       None, which means using rcParams["legend.shadow"]
                       (default: False).
        :param frame_alpha: The alpha transparency of the legend's background.
                            Default is None, which means using
                            rcParams["legend.framealpha"] (default: 0.8). If
                            shadow is activated and framealpha is None, the
                            default value is ignored.
        :param face_color: The legend's background color. Default is None, which
                           means using rcParams["legend.facecolor"]
                           (default: 'inherit'). If "inherit", use
                           rcParams["axes.facecolor"] (default: 'white').
        :param edge_color: The legend's background patch edge color. Default is
                           None, which means using rcParams["legend.edgecolor"]
                           (default: '0.8'). If "inherit", use take
                           rcParams["axes.edgecolor"] (default: 'black').
        :param mode: If mode is set to "expand" the legend will be horizontally
                     expanded to fill the axes area (or bbox_to_anchor if
                     defines the legend's size).
        :param title: The legend's title. Default is no title (None).
        :param title_font_size: The fontsize of the legend's title. Default is
                                the default fontsize.
        :param label_spacing: The fractional whitespace inside the legend border,
                              in font-size units. Default is None, which means
                              using rcParams["legend.borderpad"] (default: 0.4).
        :param handle_length: The length of the legend handles, in font-size
                              units. Default is None, which means using
                              rcParams["legend.handlelength"] (default: 2.0).
        :param handle_text_pad: The pad between the legend handle and text, in
                                font-size units. Default is None, which means
                                using rcParams["legend.handletextpad"]
                                (default: 0.8).
        :param border_axes_pad: The pad between the axes and legend border, in
                                font-size units. Default is None,
                                which means using
                                rcParams["legend.borderaxespad"] (default: 0.5).
        :param column_spacing: The spacing between columns, in font-size units.
                               Default is None, which means using
                               rcParams["legend.columnspacing"] (default: 2.0).
        """
        kwargs = {}
        for kwarg, mpl_arg in zip(
            [handles, labels, n_cols, font_properties, font_size,
             line_points, scatter_points, scatter_y_offsets, marker_scale,
             frame_on, shadow, frame_alpha, face_color, edge_color,
             mode, title, title_font_size, label_spacing, handle_length,
             handle_text_pad, border_axes_pad, column_spacing, location],
            ['handles', 'labels', 'ncol', 'prop', 'fontsize',
             'numpoints', 'scatterpoints', 'scatteryoffsets', 'markerscale',
             'frameon', 'shadow', 'framealpha', 'facecolor', 'edgecolor',
             'mode', 'title', 'title_fontsize', 'labelspacing', 'handlelength',
             'handletextpad', 'borderaxespad', 'columnspacing', 'loc']
        ):
            if kwarg is not None:
                kwargs[mpl_arg] = kwarg
        self._legend = LegendFormatter(self._axes.legend(**kwargs))
        return self._legend

    @staticmethod
    def show():
        """
        Show the figure for the axes.
        """
        plt.show()
