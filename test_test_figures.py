from matplotlib import pyplot as plt
from test_figures import Figure, assert_similar_figures
from test_test_figures_runner import run_tests

def test_line_plot_one_axes_same_plot():
    fig, ax = plt.subplots()
    ax.plot([1,2,3,4], [6,2,5,2])
    ax.legend(["This line"])
    figure = Figure(fig)

    fig2, ax2 = plt.subplots()
    ax2.plot([1,2,3,4], [6,2,5,2])
    ax.legend(["This line"])
    figure2 = Figure(fig2)

    assert_similar_figures(figure, figure2, ("x_data", "y_data"))

def test_line_plot_one_axes_dissimilar_plot():
    fig, ax = plt.subplots()
    ax.plot([1,2,3,4], [7,2,5,2])
    ax.legend(["This line"])
    figure = Figure(fig)

    fig2, ax2 = plt.subplots()
    ax2.plot([1,2,3,4], [6,2,5,2])
    ax.legend(["This line"])
    figure2 = Figure(fig2)

    assert_similar_figures(figure, figure2, ("x_data", "y_data"))

if __name__ == "__main__":
    # tests are registered in a list of tuples. The first tuple entry is the
    # function object, and the second if whether the test should fail or not
    tests = [
        (test_line_plot_one_axes_same_plot, False),
        (test_line_plot_one_axes_dissimilar_plot, True),
    ]
    run_tests(tests)
