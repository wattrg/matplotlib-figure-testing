import numpy as np
import matplotlib
from functools import total_ordering
import math

def assert_similar_figures(ref_fig, other_fig, attrs=None):
    """
    Assert that two figures are similar.

    Parameters:
        ref_fig (matplotlib figure): The reference figure
        other_fig (matplotlib figure): The figure to compare to the reference

    Raises:
        AssertionError if the figures are dissimilar
    """
    ref_fig = Figure(ref_fig)
    other_fig = Figure(other_fig)
    ref_fig.assert_similar(other_fig, attrs)


class Figure:
    """Representation of a matplotlib figure object"""
    all_attrs = ("suptitle",)
    def __init__(self, fig):
        if isinstance(fig, dict):
            self.suptitle = fig.get("suptitle")
            self.axes = [Axis(axis) for axis in fig["axes"]]
        else:
            sup_title = fig._suptitle
            if sup_title:
                self.suptitle = fig._suptitle.get_text()
            else:
                self.suptitle = ""
            self.axes = [Axis(axis) for axis in fig.get_axes()]

    def get_num_axes(self):
        """Returns the number of axes in the figure"""
        return len(self.axes)

    def assert_similar(self, other, attrs):
        """Assert that the Figure is similar to another figure"""
        if self.get_num_axes() != other.get_num_axes():
            raise AssertionError(f"Incorrect number of axes (subfigures). "
                                 f"Expected {other.get_num_axes()}, "
                                 f"found {self.get_num_axes()}")

        for attr in set(self.all_attrs).intersection(attrs):
            if getattr(self, attr) != getattr(other, attr):
                raise AssertionError(f"Incorrect {attr}. "
                                     f"Expected {getattr(other, attr)}, "
                                     f"foud {getattr(self, attr)} \n")

        for axis, other_axis in zip(self.axes, other.axes):
            axis.assert_similar(other_axis, attrs)

    def __repr__(self):
        axis_repr = repr(list([{axis} for axis in self.axes]))
        rep += f'    "suptitle": "{self.suptitle}", \n'
        rep += f'    "axes": {axis_repr}'
        return rep

class Axis:
    """Representation of a matplotlib axes object"""
    def __init__(self, ax):
        if isinstance(ax, dict):
            # We need to create an axis from a dictionary
            self.title = ax.get("title")
            self.xlabel = ax.get("xlabel")
            self.ylabel = ax.get("ylabel")
            self.xtick_label = ax.get("xtick_label")
            self.ytick_label = ax.get("ytick_label")
            self.x_scale = ax.get("x_scale")
            self.y_scale = ax.get("y_scale")
            self.legend_entries = ax.get("legend_entries")
            self.grid_spec = ax.get("grid_spec")
            # sort the lines, path_collections and patches, so that
            # the order that they get plotted in doesn't matter
            self.lines = sorted([Line(line) for line in ax.get("lines")])
            self.path_collections = sorted([PathCollection(pc)
                                     for pc in ax.get("path_collections", [])])
            self.patches = sorted([Wedge(wedge) for wedge in ax.get("wedges", [])])
        else:
            # we need to create an axis from a matplotlib axis
            self.title = ax.get_title()
            self.xlabel = ax.get_xaxis().get_label().get_text()
            self.ylabel = ax.get_yaxis().get_label().get_text()
            self.xtick_label = ax.get_xaxis().get_ticklabels()
            self.ytick_label = ax.get_yaxis().get_ticklabels()
            self.x_scale = ax.get_xscale()
            self.y_scale = ax.get_yscale()
            legend = ax.get_legend()
            if legend:
                self.legend_entries = [entry for entry in
                                       ax.get_legend().get_texts()]
            else:
                self.legend_entries = [None]
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
        rep = "{\n"
        rep += f'        "title": "{self.title}", \n'
        rep += f'        "xlabel": "{self.xlabel}", \n'
        rep += f'        "ylabel": "{self.ylabel}", \n'
        rep += f'        "xtick_label": {self.xtick_label}, \n'
        if self.ytick_label:
            rep += f'        "ytick_label": {self.ytick_label}, \n'
        rep += f'        "x_scale": "{self.x_scale}", \n'
        rep += f'        "y_scale": "{self.y_scale}", \n'
        rep += f'        "legend_entries": {repr(self.legend_entries)}, \n'
        rep += f'        "grid_spec": {self.grid_spec}, \n'
        lines_repr = repr([{line} for line in self.lines])
        rep += '        "lines": ' + f"{lines_repr},\n    "
        pc_repr = repr([{pc} for pc in self.path_collections])
        rep += f'        "path_collections": {pc_repr}\n '
        rep += "}"
        return rep

    def assert_similar(self, other, attrs):
        """Assert that the axis is similar to another axis"""
        if self.get_num_lines() != other.get_num_lines():
            raise AssertionError(f"Incorrect number of lines. "
                                 f"Expected {other.get_num_lines()}, "
                                 f"found {self.get_num_lines()}")

        if self.get_num_pc() != other.get_num_pc():
            raise AssertionError(f"Incorrect number of items in the"
                                 f"scatter plot. Expected {other.get_num_pc()} "
                                 f"found {self.get_num_pc()}")
        # test all the attributes that relate to an axes
        axis_attrs = self.__dict__.keys()
        for attr in set(attrs).intersection(axis_attrs):
            if attr in ["xtick_label", "ytick_label", "legend_entries"]:
                # It seems that matplotlib.text.Text doesn't implement __eq__
                # so here we are doing matplotlib's job for them...
                for text, text_ref in zip(getattr(self, attr),
                                          getattr(other, attr)):
                    if not check_text_equal(text, text_ref):
                        raise AssertionError(f"Incorrect {attr}: "
                                             f"'{getattr(self, attr)}', "
                                             f"Expected '{getattr(other, attr)}'")

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
        if self.patch_type != other.patch_type:
            msg = f"Incorrect shape. Expected {self.patch_type}, got {other.patch_type}"
            return False, msg
        attrs = self.all_attrs if not attrs else attrs
        for attr in set(attrs).intersection(self.all_attrs):
            if not math.isclose(getattr(self, attr), getattr(other, attr)):
                msg = f"Incorrect {self.patch_type} {attr}: {getattr(other, attr)}. "
                msg += f"Expected {getattr(self, attr)}"
                return False, msg
        return True, None

    def assert_similar(self, other, attrs=None):
        attrs = self.all_attrs if not attrs else attrs
        # first, check if the type of the patches are the same
        similar, msg = self.check_similar(other, attrs)
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
        attrs = self.all_attrs if not attrs else attrs
        for attr in set(attrs).intersection(self.all_attrs):
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
        attrs = self.all_attrs if not attrs else attrs
        similar, msg = self.check_similar(other, attrs)
        if not similar:
            raise AssertionError(msg)


@total_ordering
class Line:
    """Representation of a matplotlib line object"""
    all_attrs = ("x_data", "y_data", "linewidth", "linestyle", "marker")
    def __init__(self, line):
        if isinstance(line, dict):
            # we need to create a line from a dictionary
            self.x_data = line.get("x_data")
            self.y_data = line.get("y_data")
            self.linewidth = line.get("linewidth")
            self.linestyle = line.get("linestyle")
            self.marker = line.get("marker")
        else:
            # we probably have a matplotlib figure
            self.x_data = line.get_xdata()
            self.y_data = line.get_ydata()
            self.linewidth = line.get_linewidth()
            self.linestyle = line.get_linestyle()
            self.marker = line.get_marker()

    def __repr__(self):
        rep = f'\n            "x_data": np.{repr(self.x_data)}, \n'
        rep += f'            "y_data": np.{repr(self.y_data)}, \n'
        rep += f'            "linewidth": {self.linewidth}, \n'
        rep += f'            "linestyle": "{self.linestyle}", \n'
        rep += f'            "marker": "{self.marker}", \n        '
        return rep

    def __eq__(self, other):
        similar, _ = self.check_similar(other)
        return similar

    def __gt__(self, other):
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
        """ Check if two lines are similar """

        attrs = self.all_attrs if not attrs else attrs
        # test all the attributes that relate to a line
        line_attrs = self.__dict__.keys()
        for attr in set(attrs).intersection(line_attrs):
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
                    msg = f"A line isn't where it should be\n"
                    msg += f"Expected {attr}: {getattr(self, attr)}\n"
                    msg += f"But got {getattr(other, attr)}\n"
                    return False, msg
            else:
                # we have non numeric data, so can test exactly
                if getattr(self, attr) != getattr(other, attr):
                    msg = f"Incorrect {attr}, '{getattr(self, attr)}'."
                    msg += f"Expected '{getattr(other, attr)}'"
                    return False, msg
        return True, None

    def assert_similar(self, other, attrs=None):
        """Assert that the line is similar to another line"""

        attrs = self.all_attrs if not attrs else attrs
        similar, msg = self.check_similar(other, attrs)
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
