import numpy as np

class PathCollection:
    """
    Representation of a matplotlib PathCollection object.
    In matplotlib, PathCollection is used to define the
    data in a scatter plot
    """

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

    def assert_similar(self, other, attrs):
        """ Assert two PathCollections are similar """
        pc_attrs = self.__dict__.keys()
        for attr in set(attrs).intersection(pc_attrs):
            if attr in ["x_data", "y_data"]:
                try:
                    data_correct = np.allclose(getattr(self, attr),
                                                 getattr(other, attr))
                except ValueError:
                    data_correct = False
                finally:
                    if not data_correct:
                        raise AssertionError("Oops, scatter plot has points "
                                              "in the wrong place")
            elif attr == "marker":
                try:
                    vert_correct = np.allclose(self.marker.vertices,
                                               other.marker.vertices)
                    code_correct = np.allclose(self.marker.vertices,
                                               other.marker.vertices)
                    marker_correct = vert_correct and code_correct

                except ValueError:
                    marker_correct = False
                finally:
                    if not marker_correct:
                        raise AssertionError("Incorrect marker in scatter plot")



            elif np.all(getattr(self, attr) != getattr(other, attr)):
                raise AssertionError(f"Oops, incorrect {attr}")

class Line:
    """Representation of a matplotlib line object"""
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

    def assert_similar(self, other, attrs):
        """Assert that the line is similar to another line"""

        # test all the attributes that relate to a line
        line_attrs = self.__dict__.keys()
        for attr in set(attrs).intersection(line_attrs):
            if attr in ["x_data", "y_data"]:
                # we have numeric data, so should test if close
                # use a try except block to catch when allclose errors
                # for example when the data are different lengths
                try:
                    data_correct = np.allclose(getattr(self, attr),
                                               getattr(other, attr))
                except:
                    data_correct = False
                finally:
                    if not data_correct:
                        raise AssertionError("Oops, this line isn't where "
                                             "it should be")
            else:
                # we have non numeric data, so can test exactly
                if getattr(self, attr) != getattr(other, attr):
                    raise AssertionError(f"Incorrect {attr}, " + "'" +
                                         str(getattr(self, attr)) + "'")


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
            self.lines = [Line(line) for line in ax.get("lines")]
            self.path_collections = [PathCollection(pc)
                                     for pc in ax.get("path_collections", [])]
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
            self.lines = [Line(line) for line in ax.get_lines()]
            self.path_collections = [PathCollection(pc)
                                     for pc in ax.collections]

    def get_num_pc(self):
        """Return the number of path_collections"""
        return len(self.path_collections)

    def get_num_lines(self):
        """Get the number of lines on the axis"""
        return len(self.lines)

    def __repr__(self):
        rep = f'\n        "title": "{self.title}", \n'
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
                                     f"'{getattr(self, attr)}'.  "
                                     f"Expected '{getattr(other, attr)}'")

        # check that the lines are similar
        for line, other_line in zip(self.lines, other.lines):
            line.assert_similar(other_line, attrs)

        # check that the path collections are similar
        for pc, other_pc in zip(self.path_collections, other.path_collections):
            pc.assert_similar(other_pc, attrs)


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


class Figure:
    """Representation of a matplotlib figure object"""
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

        figure_attrs = self.__dict__.keys()
        for attr in set(figure_attrs).intersection(attrs):
            if getattr(self, attr) != getattr(other, attr):
                raise AssertionError(f"Incorrect {attr}. "
                                     f"Expected {getattr(other, attr)}, "
                                     f"foud {getattr(self, attr)} \n")

        for axis, other_axis in zip(self.axes, other.axes):
            axis.assert_similar(other_axis, attrs)

    def __repr__(self):
        axis_repr = repr(list([{axis} for axis in self.axes]))
        rep = "{\n"
        rep += f'    "suptitle": "{self.suptitle}", \n'
        rep += f'    "axes": {axis_repr}'
        rep += "}\n"
        return rep
