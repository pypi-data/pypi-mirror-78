from matplotlib.axes import Axes, SubplotBase
from matplotlib.figure import Figure
from pathlib import Path
from seaborn import JointGrid, PairGrid
from typing import Union

from mpl_format.compound_types import PlotObject


def save_plot(plot_object: PlotObject, file_path: Union[str, Path], file_type: str = 'png'):
    """
    Save a plot object to disk.

    :param plot_object: The plot object to save to disk,
    :param file_path: The file path to save the plot object to.
    :param file_type: The type of file to save.
    """
    if isinstance(file_path, Path):
        file_path = str(file_path)
    kwargs = {}
    plot_obj_type = type(plot_object)
    if plot_obj_type is Axes or issubclass(plot_obj_type, Axes) or issubclass(plot_obj_type, SubplotBase):
        fig = plot_object.figure
        kwargs['dpi'] = fig.dpi
    elif plot_obj_type is Figure:
        fig = plot_object
        kwargs['dpi'] = fig.dpi
    elif plot_obj_type in (JointGrid, PairGrid):
        fig = plot_object
    else:
        raise ValueError(
            'plot_object must be one of Axes, Figure, JointGrid, PairGrid. Type passed was %s'
            % type(plot_object)
        )
    fig.savefig(
        '%s%s' % (
            file_path,
            ('.' + file_type if not file_path.endswith('.' + file_type) else '')
        ),
        **kwargs
    )
