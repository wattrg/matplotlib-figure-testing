import numpy as np
import matplotlib
from matplotlib import pyplot as plt, _pylab_helpers
from functools import total_ordering
import math
import re


def assert_similar_figures(ref_fig, other_fig, attrs=None):
    """
    Assert that two figures are similar.

    Parameters:
        ref_fig (matplotlib figure): The reference figure
        other_fig (matplotlib figure): The figure to compare to the reference

    Raises:
        AssertionError if the figures are dissimilar
    """
    if not isinstance(ref_fig, Figure):
        ref_fig = Figure(ref_fig)
    if not isinstance(other_fig, Figure):
        other_fig = Figure(other_fig)
    ref_fig.assert_similar(other_fig, attrs)

def capture_figures(func, *args, **kwargs):
    """ 
    Runs a function which generates figures (where the function doesn't return
    the figures), gets a handle to the figures and returns them. 

    Parameters:
        func (callable): The function which generates figures
        
    Returns:
        Tuple[matplotlib.figure,...]: Handles to the figures generated by the 
        function
    """
    # Keep track of the original figures
    original_figs = _pylab_helpers.Gcf.figs.copy()

    # determine if matplotlib is in interactive mode
    interactive = matplotlib.is_interactive()

    # Turning interactive mode on means plt.show() is non-blocking,
    # and won't clear the active figures on calling plt.show()
    if not interactive:
        plt.ion()

    # close existing figures, so that we don't get confused by them
    plt.close("all")

    # call the function which generates the figures
    func(*args, **kwargs)

    # get handles to the figures
    fig_managers = _pylab_helpers.Gcf.get_all_fig_managers() 
    figs = []
    for fig_manager in fig_managers:
        figs.append(fig_manager.canvas.figure)

    # restore interactive mode to its original state
    if not interactive:
        plt.ioff()

    # reset the figure manager to its original state, as if we
    # were never here
    _pylab_helpers.Gcf.figs = original_figs

    # we're done!
    return tuple(figs)

class Figure:
    """Representation of a matplotlib figure object"""
    all_attrs = ("suptitle", "has_suptitle")
    def __init__(self, fig):
        if isinstance(fig, dict):
            self.suptitle = fig.get("suptitle")
            self.has_suptitle = fig.get("has_suptitle", False)
            self.axes = [axis for axis in fig["axes"]]
        else:
            sup_title = fig._suptitle
            if sup_title:
                self.suptitle = fig._suptitle.get_text()
                self.has_suptitle = True
            else:
                self.suptitle = ""
                self.has_suptitle = False
            self.axes = [Axis(axis) for axis in fig.get_axes()]

    def get_num_axes(self):
        """Returns the number of axes in the figure"""
        return len(self.axes)

    def assert_similar(self, other, attrs=None):
        """Assert that the Figure is similar to another figure"""

        test_attrs = self.all_attrs if not attrs else attrs
        if self.get_num_axes() != other.get_num_axes():
            raise AssertionError(f"Incorrect number of axes (subfigures). "
                                 f"Expected {other.get_num_axes()}, "
                                 f"found {self.get_num_axes()}")

        for attr in set(self.all_attrs).intersection(test_attrs):
            if getattr(self, attr) != getattr(other, attr):
                raise AssertionError(f"Incorrect {attr}. "
                                     f"Expected {getattr(other, attr)}, "
                                     f"foud {getattr(self, attr)} \n")

        for axis, other_axis in zip(self.axes, other.axes):
            axis.assert_similar(other_axis, attrs)

    def __repr__(self):
        axis_repr = repr(list([axis for axis in self.axes]))
        rep = "Figure({\n"
        rep += f'    "suptitle": "{self.suptitle}", \n'
        rep += f'    "has_suptitle": {self.has_suptitle},\n'
        rep += f'    "axes": {axis_repr}\n'
        rep += "})"
        return rep

    def write_to_file(self, var_name, filename):
        """ Writes a figure object to a file """
        with open(filename, "w") as f:
            f.write("from matplotlib_figure_testing.test_figures import *\n")
            f.write("from matplotlib.text import Text\n")
            f.write(f"{var_name} = {self}")

class Axis:
    """Representation of a matplotlib axes object"""
    all_attrs = ("title", "has_title", "xlabel", "has_xlabel", "ylabel", "has_ylabel",
                 "xtick_label", "ytick_label", "x_scale", "y_scale", "legend_entries",
                 "num_legend_entries", "grid_spec")
    def __init__(self, ax):
        if isinstance(ax, dict):
            # We need to create an axis from a dictionary
            self.title = ax.get("title")
            self.has_title = ax.get("has_title")
            self.xlabel = ax.get("xlabel")
            self.has_xlabel = ax.get("has_xlabel", False)
            self.ylabel = ax.get("ylabel")
            self.has_ylabel = ax.get("has_ylabel", False)
            self.xtick_label = ax.get("xtick_label")
            self.ytick_label = ax.get("ytick_label")
            self.x_scale = ax.get("x_scale")
            self.y_scale = ax.get("y_scale")
            self.legend_entries = ax.get("legend_entries")
            self.num_legend_entries = ax.get("num_legend_entries")
            self.grid_spec = ax.get("grid_spec")
            # sort the lines, path_collections and patches, so that
            # the order that they get plotted in doesn't matter
            self.lines = sorted([line for line in ax.get("lines")])
            self.path_collections = sorted([PathCollection(pc)
                                     for pc in ax.get("path_collections", [])])
            self.patches = sorted([patch for patch in ax.get("patches", [])])
        else:
            # we need to create an axis from a matplotlib axis
            self.title = ax.get_title()
            self.has_title = False if self.title == "" else True
            self.xlabel = ax.get_xaxis().get_label().get_text()
            self.has_xlabel = False if self.xlabel == "" else True
            self.ylabel = ax.get_yaxis().get_label().get_text()
            self.has_ylabel = False if self.ylabel == "" else True
            self.xtick_label = ax.get_xaxis().get_ticklabels()
            self.ytick_label = ax.get_yaxis().get_ticklabels()
            self.x_scale = ax.get_xscale()
            self.y_scale = ax.get_yscale()
            legend = ax.get_legend()
            if legend:
                self.legend_entries = [entry for entry in
                                       ax.get_legend().get_texts()]
                self.num_legend_entries = len(self.legend_entries)
            else:
                self.legend_entries = [None]
                self.num_legend_entries = 0
            self.grid_spec = ax.get_gridspec().get_geometry()
            # sort the lines, path_collections and patches, so that
            # the order that they get plotted in doesn't matter
            self.lines = sorted([Line(line) for line in ax.get_lines()])
            self.path_collections = sorted([PathCollection(pc)
                                     for pc in ax.collections])
            self.patches = sorted([create_patch(patch) for patch in ax.patches])

    def get_num_pc(self):
        """Return the number of path_collections"""
        return len(self.path_collections)

    def get_num_lines(self):
        """Get the number of lines on the axis"""
        return len(self.lines)

    def __repr__(self):
        rep = "Axis({\n"
        rep += f'        "title": "{self.title}", \n'
        rep += f'        "has_title": {self.has_title}, \n'
        rep += f'        "xlabel": "{self.xlabel}", \n'
        rep += f'        "has_xlabel": {self.has_xlabel}, \n'
        rep += f'        "ylabel": "{self.ylabel}", \n'
        rep += f'        "has_ylabel": {self.has_ylabel}, \n'
        rep += f'        "xtick_label": {self.xtick_label}, \n'
        if self.ytick_label:
            rep += f'        "ytick_label": {self.ytick_label}, \n'
        rep += f'        "x_scale": "{self.x_scale}", \n'
        rep += f'        "y_scale": "{self.y_scale}", \n'
        rep += f'        "legend_entries": {repr(self.legend_entries)}, \n'
        rep += f'        "num_legend_entries": {self.num_legend_entries},\n'
        rep += f'        "grid_spec": {self.grid_spec}, \n'
        lines_repr = repr([line for line in self.lines])
        rep += '        "lines": ' + f"{lines_repr},\n"
        pc_repr = repr([{pc} for pc in self.path_collections])
        rep += f'        "path_collections": {pc_repr},\n'
        patch_repr = repr([patch for patch in self.patches])
        rep += f'        "patches": {patch_repr},\n'
        rep += "    }),\n"
        return rep

    def assert_similar(self, other, attrs=None):
        """Assert that the axis is similar to another axis"""
        test_attrs = self.all_attrs if not attrs else attrs
        if self.get_num_lines() != other.get_num_lines():
            raise AssertionError(f"Incorrect number of lines. "
                                 f"Expected {self.get_num_lines()}, "
                                 f"found {other.get_num_lines()}")

        if self.get_num_pc() != other.get_num_pc():
            raise AssertionError(f"Incorrect number of items in the"
                                 f"scatter plot. Expected {self.get_num_pc()} "
                                 f"found {other.get_num_pc()}")
        # test all the attributes that relate to an axes
        for attr in set(test_attrs).intersection(self.all_attrs):
            if attr in ["xtick_label", "ytick_label", "legend_entries"]:
                # It seems that matplotlib.text.Text doesn't implement __eq__
                # so here we are doing matplotlib's job for them...
                for text, text_ref in zip(getattr(self, attr),
                                          getattr(other, attr)):
                    if not check_text_equal(text, text_ref):
                        raise AssertionError(f"Incorrect {attr}: "
                                             f"'{getattr(other, attr)}', "
                                             f"Expected '{getattr(self, attr)}'")

            elif getattr(self, attr) != getattr(other, attr):
                raise AssertionError(f"Incorrect {attr}, "
                                     f"'{getattr(other, attr)}'.  "
                                     f"Expected '{getattr(self, attr)}'")

        # check that the lines are similar. The lines may be in a different order
        for line, other_line in zip(self.lines, other.lines):
            line.assert_similar(other_line, attrs)

        # check that the path collections are similar
        for pc, other_pc in zip(self.path_collections, other.path_collections):
            pc.assert_similar(other_pc, attrs)

        # check that the patches are similar
        for patch, other_patch in zip(self.patches, other.patches):
            patch.assert_similar(other_patch, attrs)

def create_patch(patch):
    if isinstance(patch, matplotlib.patches.Wedge):
        return Wedge(patch)
    elif isinstance(patch, matplotlib.patches.Rectangle):
        return Rectangle(patch)

class Patch:
    """
    Representation of a matplotlib patch
    """
    def check_similar(self, other, attrs=None):
        test_attrs = self.all_attrs if not attrs else attrs
        if self.patch_type != other.patch_type:
            msg = f"Incorrect shape. Expected {self.patch_type}, got {other.patch_type}"
            return False, msg
        test_attrs = self.all_attrs if not attrs else attrs
        for attr in set(test_attrs).intersection(self.all_attrs):
            if not math.isclose(getattr(self, attr), getattr(other, attr)):
                msg = f"Incorrect {self.patch_type} {attr}: {getattr(other, attr)}. "
                msg += f"Expected {getattr(self, attr)}"
                return False, msg
        return True, None

    def assert_similar(self, other, attrs=None):
        test_attrs = self.all_attrs if not attrs else attrs
        similar, msg = self.check_similar(other, test_attrs)
        if not similar:
            raise AssertionError(msg)

    def __eq__(self, other):
        similar, _ = self.check_similar(other)
        return similar

    def __gt__(self, other):
        for attr in self.all_attrs:
            if getattr(self, attr) > getattr(other, attr):
                return True
            elif getattr(self, attr) < getattr(other, attr):
                return False
        return False


@total_ordering
class Rectangle(Patch):
    """
    Representation of a matplotlib Rectangle patch
    """
    patch_type = "rectangle"
    all_attrs = ("height", "width", "position_x", "position_y")

    def __init__(self, rectangle):
        if isinstance(rectangle, dict):
            self.height = rectangle.get("height")
            self.width = rectangle.get("width")
            self.position_x, self.position_y = rectangle.get("position_x"), rectangle.get("position_y")
        else:
            self.height = rectangle.get_height()
            self.width = rectangle.get_width()
            self.position_x, self.position_y = rectangle.get_xy()

    def __repr__(self):
        rep = "Rectangle({"
        rep += f"'height': {self.height}, "
        rep += f"'width': {self.width}, "
        rep += f"'position_x': {self.position_x}, "
        rep += f"'position_y': {self.position_y}, "
        rep += "})"
        return rep

@total_ordering
class Wedge(Patch):
    """
    Representation of a matplotlib Wedge patch
    """
    patch_type = "wedge"
    all_attrs = ("theta", "r", "theta1", "theta2", "center_x", "center_y")

    def __init__(self, wedge):
        if isinstance(wedge, dict):
            self.r = wedge.get("r")
            self.theta1 = wedge.get("theta1")
            self.theta2 = wedge.get("theta2")
            self.center_x, self.center_y = wedge.get("center_x"), wedge.get("center_y")
            self.theta = abs(self.theta1 - self.theta2)
        else:
            self.r = wedge.r
            self.theta1 = wedge.theta1
            self.theta2 = wedge.theta2
            self.center_x, self.center_y = wedge.center
            self.theta = abs(wedge.theta1 - wedge.theta2)

    def __repr__(self):
        rep = "Wedge({"
        rep += f"'r': {self.r}, "
        rep += f"'theta1': {self.theta1}, "
        rep += f"'theta2': {self.theta2}, "
        rep += f"'theta': {self.theta}, "
        rep += f"'center_x': {self.center_x}, "
        rep += f"'center_y': {self.center_y}"
        rep += "})"
        return rep


@total_ordering
class PathCollection:
    """
    Representation of a matplotlib PathCollection object.
    In matplotlib, PathCollection is used to define the
    data in a scatter plot
    """
    all_attrs = ("x_data", "y_data", "marker")
    def __init__(self, pc):
        if isinstance(pc, dict):
            self.x_data = pc.get("x_data")
            self.y_data = pc.get("y_data")
            self.marker = pc.get("marker")
        else:
            data = pc.get_offsets().data
            self.x_data = data[:, 0]
            self.y_data = data[:, 1]
            self.marker = pc.get_paths()[0]

    def __repr__(self):
        rep = f'\n        "x_data": np.{repr(self.x_data)}, \n'
        rep += f'        "y_data": np.{repr(self.y_data)}, \n'
        rep += f'        "marker": {self.marker}'
        return rep

    def __eq__(self, other):
        eq, _ = self.check_similar(other)
        if eq:
            return True
        return False

    def __gt__(self, other):
        if self.marker.vertices.tolist() > other.marker.vertices.tolist():
            return True
        if self.marker.vertices.tolist() < other.marker.vertices.tolist():
            return False
        if list(self.x_data) > list(other.x_data):
            return True
        if list(self.x_data) < list(other.x_data):
            return False
        if list(self.y_data) > list(other.y_data):
            return True
        if list(self.y_data) < list(other.y_data):
            return False
        return False

    def check_similar(self, other, attrs=None):
        """ Check if two PathCollections are similar """
        test_attrs = self.all_attrs if not attrs else attrs
        for attr in set(test_attrs).intersection(self.all_attrs):
            if attr in ("x_data", "y_data"):
                try:
                    data_correct = np.allclose(getattr(self, attr),
                                                 getattr(other, attr))
                except ValueError:
                    data_correct = False
                finally:
                    if not data_correct:
                        msg = "Scatter plot has points in the wrong place"
                        return False, msg
            elif attr == "marker":
                try:
                    vert_correct = np.allclose(self.marker.vertices,
                                               other.marker.vertices)
                    code_correct = np.allclose(self.marker.vertices,
                                               other.marker.vertices)
                    marker_correct = vert_correct and code_correct

                except ValueError:
                    marker_correct = False
                if not marker_correct:
                    return False, "Incorrect marker in scatter plot"
        return True, None


    def assert_similar(self, other, attrs=None):
        """ Assert two PathCollections are similar """
        test_attrs = self.all_attrs if not attrs else attrs
        similar, msg = self.check_similar(other, test_attrs)
        if not similar:
            raise AssertionError(msg)

def numpy_array_gt(array1, array2):
    for i, j in zip(array1, array2):
        if i > j:
            return True
        if i < j:
            return False
    return False

def numpy_array_lt(array1, array2):
    for i, j in zip(array1, array2):
        if i < j:
            return True
        if i > j:
            return False
    return False

@total_ordering
class Line:
    """Representation of a matplotlib line object"""
    all_attrs = ("x_data", "y_data", "linewidth",
                 "linestyle", "marker", "colour", "label")
    def __init__(self, line):
        if isinstance(line, dict):
            # we need to create a line from a dictionary
            self.x_data = line.get("x_data")
            self.y_data = line.get("y_data")
            self.linewidth = line.get("linewidth", 1.5)
            self.linestyle = line.get("linestyle", "")
            self.marker = line.get("marker", "")
            self.colour = line.get("colour", "")
            self.label = line.get("label", "")
        else:
            # we probably have a matplotlib figure
            self.x_data = line.get_xdata()
            self.y_data = line.get_ydata()
            self.linewidth = line.get_linewidth()
            self.linestyle = line.get_linestyle()
            self.marker = line.get_marker()
            self.colour = matplotlib.colors.to_hex(line.get_color())
            self.label = line.get_label()
            # the default label seems to be _child0, _child1,...
            # so if the label matches that pattern,
            # set the label to an empty string
            if re.match(r"^_child[0-9]+$", self.label):
                self.label = ""

    def __repr__(self):
        rep = "Line({\n"
        rep += f'            "x_data": np.{repr(self.x_data)}, \n'
        rep += f'            "y_data": np.{repr(self.y_data)}, \n'
        rep += f'            "linewidth": {self.linewidth}, \n'
        rep += f'            "linestyle": "{self.linestyle}", \n'
        rep += f'            "marker": "{self.marker}", \n        '
        rep += f'            "colour": "{self.colour}",\n'
        rep += f'            "label": "{self.label}",\n'
        rep += "        })"
        return rep

    def __eq__(self, other):
        similar, _ = self.check_similar(other)
        return similar

    def __gt__(self, other):
        if numpy_array_gt(self.x_data, other.x_data):
            return True
        if numpy_array_lt(self.x_data, other.x_data):
            return False
        if numpy_array_gt(self.y_data, other.y_data):
            return True
        if numpy_array_lt(self.y_data, other.y_data):
            return False
        if self.label > other.label:
            return True
        if self.label < other.label:
            return False
        if self.colour > other.colour:
            return True
        if self.colour < other.colour:
            return False
        if self.linewidth > other.linewidth:
            return True
        if self.linewidth < other.linewidth:
            return False
        if self.linestyle > other.linestyle:
            return True
        if self.linestyle < other.linestyle:
            return False
        if (self.marker is not None) and (other.marker is not None) and (self.marker > other.marker):
            return True
        if (self.marker is not None) and (other.marker is not None) and (self.marker < other.marker):
            return False
        return False

    def check_similar(self, other, attrs=None):
        """ Check if two lines are similar """

        test_attrs = self.all_attrs if not attrs else attrs
        # test all the attributes that relate to a line
        for attr in set(test_attrs).intersection(self.all_attrs):
            if attr in ("x_data", "y_data"):
                # we have numeric data, so should test if close
                # use a try except block to catch when allclose errors
                # for example when the data are different lengths
                try:
                    data_correct = np.allclose(getattr(self, attr),
                                               getattr(other, attr))
                except:
                    data_correct = False

                if not data_correct:
                    msg  = f"A line (colour='{self.colour}', "
                    msg += f"label='{self.label}', "
                    msg += f"linestyle='{self.linestyle}', "
                    msg += f"linewidth={self.linewidth}) "
                    msg +=  "isn't where it should be\n"
                    msg += f"Expected {attr}: {getattr(self, attr)}\n"
                    msg += f"But got {getattr(other, attr)}\n"
                    return False, msg
            else:
                # we have non numeric data, so can test exactly
                if getattr(self, attr) != getattr(other, attr):
                    msg = f"Incorrect {attr}, '{getattr(other, attr)}'."
                    msg += f"Expected '{getattr(self, attr)}'"
                    return False, msg
        return True, None

    def assert_similar(self, other, attrs=None):
        """Assert that the line is similar to another line"""

        test_attrs = self.all_attrs if not attrs else attrs
        similar, msg = self.check_similar(other, test_attrs)
        if not similar:
            raise AssertionError(msg)


def check_text_equal(text, ref_text):
    """Check if two matplotlib.text.Text objects are equal"""
    if text is None and ref_text is None:
        return True
    if text is None and ref_text is not None:
        return False
    if ref_text is None and text is not None:
        return False
    if text.get_position() != ref_text.get_position():
        return False
    if text.get_text() != ref_text.get_text():
        return False
    return True
