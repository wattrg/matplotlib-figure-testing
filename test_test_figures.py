from matplotlib import pyplot as plt
from test_figures import assert_similar_figures
from test_test_figures_runner import run_tests

def test_line_plot_one_axes_same_plot():
    fig, ax = plt.subplots()
    ax.plot([1,2,3,4], [6,2,5,2])
    ax.legend(["This line"])

    fig2, ax2 = plt.subplots()
    ax2.plot([1,2,3,4], [6,2,5,2])
    ax.legend(["This line"])

    assert_similar_figures(fig, fig2, ("x_data", "y_data"))

def test_line_plot_one_axes_dissimilar_plot():
    fig, ax = plt.subplots()
    ax.plot([1,2,3,4], [7,2,5,2])
    ax.legend(["This line"])

    fig2, ax2 = plt.subplots()
    ax2.plot([1,2,3,4], [6,2,5,2])
    ax.legend(["This line"])

    assert_similar_figures(fig, fig2, ("x_data", "y_data"))

def test_wedge_similar():
    fig, ax = plt.subplots()
    ax.pie([5, 6, 7, 8])

    fig2, ax2 = plt.subplots()
    ax2.pie([5, 6, 7, 8])

    assert_similar_figures(fig, fig2, ("r", "theta1", "theta2"))

def test_wedge_dissimilar():
    fig, ax = plt.subplots()
    ax.pie([5, 6, 7, 8])

    fig2, ax2 = plt.subplots()
    ax2.pie([6, 6, 7, 8])

    assert_similar_figures(fig, fig2, ("r", "theta1", "theta2"))

if __name__ == "__main__":
    # tests are registered in a list of tuples. The first tuple entry is the
    # function object, and the second is whether the test should produce an error
    tests = [
        (test_line_plot_one_axes_same_plot, False),
        (test_line_plot_one_axes_dissimilar_plot, True),
        (test_wedge_similar, False),
        (test_wedge_dissimilar, True),
    ]
    run_tests(tests)
