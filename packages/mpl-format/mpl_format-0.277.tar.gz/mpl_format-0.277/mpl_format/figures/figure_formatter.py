from pathlib import Path
from typing import Tuple, Union, Callable, List, Optional, TypeVar

import matplotlib.pyplot as plt
from matplotlib.axes import Axes
from matplotlib.figure import Figure
from numpy import ndarray, reshape

from mpl_format.axes.axes_formatter import AxesFormatter
from mpl_format.axes.axes_formatter_array import AxesFormatterArray
from mpl_format.compound_types import StringMapper
from mpl_format.io_utils import save_plot


TextSetter = TypeVar(
    'TextSetter',
    str, List[str], Callable[[int, int], str], Callable[[int], str]
)


class FigureFormatter(object):

    share_values = ('all', 'row', 'col', 'none')

    def __init__(self, fig_or_axes: Union[Figure, Axes] = None,
                 n_rows: int = 1, n_cols: int = 1,
                 fig_size: Tuple[int, int] = (16, 9),
                 share_x: str = 'none',
                 share_y: str = 'none',
                 constrained_layout: bool = True):

        if fig_or_axes is not None:
            if isinstance(fig_or_axes, Figure):
                self._figure = fig_or_axes
                axes_list = self._figure.axes
                rows_cols = (
                    axes_list[0].get_subplotspec().get_topmost_subplotspec()
                                .get_gridspec().get_geometry()
                )
                self._axes = reshape(axes_list, rows_cols)
            elif isinstance(fig_or_axes, Axes):
                self._figure = fig_or_axes.figure
                self._axes = fig_or_axes
            else:
                raise ValueError('Can only instantiate a new FigureFormatter '
                                 'from an Axes or Figure instance.')
        else:
            assert share_x in self.share_values
            assert share_y in self.share_values
            self._fig_size: Tuple[int, int] = fig_size
            figure, axes = plt.subplots(
                nrows=n_rows, ncols=n_cols,
                sharex=share_x, sharey=share_y,
                figsize=fig_size,
                constrained_layout=constrained_layout
            )
            self._axes: Union[Axes, ndarray] = axes
            self._figure: Figure = figure
        self._has_array = (
                isinstance(self._axes, ndarray) or isinstance(self._axes, list)
        )

    @property
    def axes(self) -> Union[AxesFormatter, AxesFormatterArray]:
        """
        Return an AxesFormatter or AxesFormatterArray for the wrapped Axes or
        array of Axes.
        """
        if not self._has_array:
            return AxesFormatter(self._axes)
        else:
            return AxesFormatterArray(self._axes)

    @property
    def figure(self) -> Figure:
        return self._figure

    @property
    def single(self) -> AxesFormatter:
        """
        Return an AxesFormatter for the wrapped Axes.
        """
        if not self._has_array:
            return AxesFormatter(self._axes)
        else:
            raise TypeError('FigureFormatter holds an array of Axes.')

    @property
    def multi(self) -> AxesFormatterArray:
        """
        Return an AxesFormatterArray for the wrapped Axes.
        """
        if self._has_array:
            return AxesFormatterArray(self._axes)
        else:
            raise TypeError('FigureFormatter holds a single Axes.')

    def _set_text_property(
            self,
            text: TextSetter,
            method: Callable[[AxesFormatter, str], AxesFormatter]
    ) -> 'FigureFormatter':
        """
        Set a text property of each Axes using a string, list of strings,
        or function that returns a string based on the row and column or the
        flat index of the Axes.

        :param text: Title or titles to set
        :param method: Method to call to format the text.
        """
        if not self._has_array:
            if not isinstance(text, str):
                raise TypeError('text must be a str for a single Axes.')
            else:
                method(self.single, text)
        else:
            if isinstance(text, str):
                for axf in self.multi.flat:
                    method(axf, text)
            elif isinstance(text, list):
                if len(text) != self.multi.size:
                    raise ValueError(f'There are {self.multi.size} Axes'
                                     f' and {len(text)} strings.')
                else:
                    for axf, t in zip(self.multi.flat, text):
                        method(axf, t)
            elif callable(text):
                try:
                    for row in range(self.multi.shape[0]):
                        for col in range(self.multi.shape[1]):
                            method(self.multi[row, col], text(row, col))
                except TypeError:
                    for a, axf in enumerate(self.multi.flat):
                        method(axf, text(a))
            else:
                raise TypeError(
                    f'Wrong type passed to _set_text_property: {type(text)}'
                )
        return self

    def set_axes_title_text(
            self,
            text: TextSetter
    ) -> 'FigureFormatter':
        """
        Set the title text of each Axes using a string, list of strings,
        or function that returns a string based on the row and column or the
        flat index of the Axes.

        :param text: Title or titles to set.
        """
        def set_text(
                axes_formatter: AxesFormatter, string: str
        ) -> AxesFormatter:
            return axes_formatter.set_title_text(string)

        self._set_text_property(text=text, method=set_text)
        return self

    def set_axes_x_label_text(
            self,
            text: TextSetter
    ) -> 'FigureFormatter':
        """
        Set the x-label text of each Axes using a string, list of strings,
        or function that returns a string based on the row and column or the
        flat index of the Axes.

        :param text: Label or labels to set.
        """
        def set_text(
                axes_formatter: AxesFormatter, string: str
        ) -> AxesFormatter:
            return axes_formatter.set_x_label_text(string)

        self._set_text_property(text=text, method=set_text)
        return self

    def set_axes_y_label_text(
            self, text: TextSetter
    ) -> 'FigureFormatter':
        """
        Set the x-label text of each Axes using a string, list of strings,
        or function that returns a string based on the row and column or the
        flat index of the Axes.

        :param text: Label or labels to set.
        """
        def set_text(
                axes_formatter: AxesFormatter, string: str
        ) -> AxesFormatter:
            return axes_formatter.set_y_label_text(string)

        self._set_text_property(text=text, method=set_text)
        return self

    def set_axes_text(
            self,
            title: Optional[TextSetter] = None,
            x_label: Optional[TextSetter] = None,
            y_label: Optional[TextSetter] = None
    ) -> 'FigureFormatter':
        """
        Set the text for each Axes' title, x_label or y_label.

        :param title: Axes titles.
        :param x_label: Axes x-labels.
        :param y_label: Axes y-labels.
        """
        if title is not None:
            self.set_axes_title_text(title)
        if x_label is not None:
            self.set_axes_x_label_text(x_label)
        if y_label is not None:
            self.set_axes_y_label_text(y_label)
        return self

    def map_axes_title_text(
            self, mapping: StringMapper
    ) -> 'FigureFormatter':
        """
        Map the label text for the x-axis using a dictionary or function.

        :param mapping: Dictionary or a function mapping old text to new text.
        """
        if not self._has_array:
            self.single.map_title_text(mapping=mapping)
        else:
            for axf in self.multi.flat:
                axf.map_title_text(mapping=mapping)
        return self

    def remove_x_axis_labels(self) -> 'FigureFormatter':
        """
        Remove the x-axis label for each Axes in the Figure.
        """
        if self._has_array:
            for axf in self.multi.flat:
                axf.remove_x_label()
        else:
            self.single.remove_x_label()
        return self

    def remove_y_axis_labels(self) -> 'FigureFormatter':
        """
        Remove the x-axis label for each Axes in the Figure.
        """
        if self._has_array:
            for axf in self.multi.flat:
                axf.remove_y_label()
        else:
            self.single.remove_y_label()
        return self

    def remove_axes_labels(self) -> 'FigureFormatter':
        """
        Remove the x-axis label for each Axes in the Figure.
        """
        self.remove_x_axis_labels()
        self.remove_y_axis_labels()
        return self

    def map_x_axis_labels(
            self, mapping: StringMapper
    ) -> 'FigureFormatter':
        """
        Map the label text for each x-axis in the Figure using a dictionary
        or function.

        :param mapping: Dictionary or a function mapping old text to new text.
        """
        if self._has_array:
            for axf in self.multi.flat:
                axf.map_x_axis_label(mapping=mapping)
        else:
            self.single.map_x_axis_label(mapping=mapping)
        return self

    def map_y_axis_labels(
            self, mapping: StringMapper
    ) -> 'FigureFormatter':
        """
        Map the label text for each y-axis in the Figure using a dictionary
        or function.

        :param mapping: Dictionary or a function mapping old text to new text.
        """
        if self._has_array:
            for axf in self.multi.flat:
                axf.map_y_axis_label(mapping=mapping)
        else:
            self.single.map_y_axis_label(mapping=mapping)
        return self

    def map_axes_labels(
            self, mapping: StringMapper
    ) -> 'FigureFormatter':
        """
        Map the label text for each axis in the Figure using a dictionary
        or function.

        :param mapping: Dictionary or a function mapping old text to new text.
        """
        self.map_x_axis_labels(mapping=mapping)
        self.map_y_axis_labels(mapping=mapping)
        return self

    def wrap_x_axis_labels(self, max_width: int) -> 'FigureFormatter':
        """
        Wrap the text for each X-Axis label if it exceeds a given width
        of characters.

        :param max_width: The maximum character width per line.
        """
        if self._has_array:
            for axf in self.multi.flat:
                axf.wrap_x_label(max_width=max_width)
        else:
            self.single.wrap_x_label(max_width=max_width)
        return self

    def wrap_y_axis_labels(self, max_width: int) -> 'FigureFormatter':
        """
        Wrap the text for each Y-Axis label if it exceeds a given width
        of characters.

        :param max_width: The maximum character width per line.
        """
        if self._has_array:
            for axf in self.multi.flat:
                axf.wrap_y_label(max_width=max_width)
        else:
            self.single.wrap_y_label(max_width=max_width)
        return self

    def wrap_axes_labels(self, max_width: int) -> 'FigureFormatter':
        """
        Wrap the text for each Axis label if it exceeds a given width
        of characters.

        :param max_width: The maximum character width per line.
        """
        self.wrap_x_axis_labels(max_width=max_width)
        self.wrap_y_axis_labels(max_width=max_width)
        return self

    def wrap_axes_titles(self, max_width: int) -> 'FigureFormatter':
        """
        Wrap the text for each Axes title if it exceeds a given width
        of characters.

        :param max_width: The maximum character width per line.
        """
        if not self._has_array:
            self.single.wrap_title(max_width=max_width)
        else:
            for axf in self.multi.flat:
                axf.wrap_title(max_width=max_width)
        return self

    def subplots_adjust(
            self,
            left: Optional[float] = None, right: Optional[float] = None,
            top: Optional[float] = None, bottom: Optional[float] = None,
            w_space: Optional[float] = None, h_space: Optional[float] = None
    ) -> 'FigureFormatter':
        """
        Adjust the padding of the Figure.

        :param left: The position of the left edge of the subplots,
                     as a fraction of the figure width.
        :param right: The position of the right edge of the subplots,
                      as a fraction of the figure width.
        :param top: The position of the top edge of the subplots,
                    as a fraction of the figure height.
        :param bottom: The position of the bottom edge of the subplots,
                       as a fraction of the figure height.
        :param w_space: The width of the padding between subplots,
                        as a fraction of the average axes width.
        :param h_space: The height of the padding between subplots,
                        as a fraction of the average axes height.
        """
        self.figure.subplots_adjust(
            left=left, right=right,
            bottom=bottom, top=top,
            wspace=w_space, hspace=h_space
        )
        return self

    def save(
            self, file_path: Union[str, Path], file_type: str = 'png'
    ) -> 'FigureFormatter':
        """
        Save the plot to disk.

        :param file_path: The file path to save the plot object to.
        :param file_type: The type of file to save.
        """
        save_plot(plot_object=self._figure,
                  file_path=file_path, file_type=file_type)
        return self

    @staticmethod
    def show():
        """
        Show the figure.
        """
        plt.show()

    def __getitem__(self, *args, **kwargs) -> AxesFormatter:

        return self.multi.__getitem__(*args, **kwargs)
