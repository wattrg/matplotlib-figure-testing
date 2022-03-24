# matplotlib-figure-testing
Test that two matplotlib figures are similar, in the sense that a list of attributes of the figures are the same.

## Usage
To use these tests, you need only import one function:
```
from test_figures import assert_similar_figures
```
Then compare `ref_fig` and `other_fig` with 
```
assert_similar_figures(ref_fig, other_fig[, attrs])
```
Where `attrs` is a tuple of attributes you would like to compare. Possible entries are:
* `"x_data"`
* `"y_data"`
* `"legend"`
* `"linewidth"`
* `"linestyle"`
* `"x_scale"`
* `"y_scale"`
* `"legend_entries"`
* `"grid_spec"`
* `"title"`
* `"suptitle"`
* `"x_label"`
* `"y_label"`
* `"marker"`
* `"width"` (for rectangle patches)
* `"height"` (for rectangle patches)
* `"position_x"` (for rectangle patches)
* `"position_y"` (for rectangle patches)
* `"theta1"` (for wedge patches)
* `"theta2"` (for wedge patches)
* `"theta"` (for wedge patches)
* `"center_x"` (for wedge patches)
* `"center_y"` (for wedge patches)
* `"r"` (for wedge patches)

If a provided attribute doesn't make sense for the particular object being compared, it will be ignored. If `attrs` is not provided, all the relevent attributes will be tested.
