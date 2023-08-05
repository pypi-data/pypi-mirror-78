from matplotlib.axes import Axes
from matplotlib.figure import Figure
from seaborn import JointGrid, PairGrid
from typing import TypeVar, Tuple, Union, Dict, Callable

Color = TypeVar('Color', str, Tuple[float, float, float, float])
FontSize = TypeVar('FontSize', str, float, int)
LegendLocation = TypeVar('LegendLocation', str, Tuple[float, float])
PlotObject = TypeVar('PlotObject', Axes, Figure, JointGrid, PairGrid)
StringMapper = Union[Dict[str, str], Callable[[str], str]]
