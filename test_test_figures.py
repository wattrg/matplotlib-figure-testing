from matplotlib import pyplot as plt
from test_figures import assert_similar_figures
from test_test_figures_runner import run_tests, register_test

@register_test()
def test_line_plot_one_axes_same_plot():
    fig, ax = plt.subplots()
    ax.plot([1,2,3,4], [6,2,5,2])
    ax.legend(["This line"])

    fig2, ax2 = plt.subplots()
    ax2.plot([1,2,3,4], [6,2,5,2])
    ax.legend(["This line"])

    assert_similar_figures(fig, fig2, ("x_data", "y_data", "legend"))

@register_test(should_fail=True)
def test_line_plot_one_axes_dissimilar_plot():
    fig, ax = plt.subplots()
    ax.plot([1,2,3,4], [7,2,5,2])
    ax.legend(["This line"])

    fig2, ax2 = plt.subplots()
    ax2.plot([1,2,3,4], [6,2,5,2])
    ax.legend(["This line"])

    assert_similar_figures(fig, fig2, ("x_data", "y_data"))

@register_test()
def test_pie_similar():
    fig, ax = plt.subplots()
    ax.pie([5, 6, 7, 8])

    fig2, ax2 = plt.subplots()
    ax2.pie([5, 6, 7, 8])

    assert_similar_figures(fig, fig2, ("r", "theta1", "theta2", "center"))

@register_test(should_fail=True)
def test_pie_dissimilar():
    fig, ax = plt.subplots()
    ax.pie([5, 6, 7, 8])

    fig2, ax2 = plt.subplots()
    ax2.pie([6, 6, 7, 8])

    assert_similar_figures(fig, fig2, ("r", "theta1", "theta2", "center"))

@register_test()
def test_bar_similar():
    fig, ax = plt.subplots()
    ax.bar([1, 2, 3], [6, 7, 8])

    fig2, ax2 = plt.subplots()
    ax2.bar([1, 2, 3], [6, 7, 8])

    assert_similar_figures(fig, fig2, ("width", "height", "position"))

@register_test(should_fail=True)
def test_bar_dissimilar():
    fig, ax = plt.subplots()
    ax.bar([1, 2, 3], [5,8,1])

    fig2, ax2 = plt.subplots()
    ax2.bar([1, 2, 3], [6,8,1])

    assert_similar_figures(fig, fig2, ("width", "height", "position"))

if __name__ == "__main__":
    run_tests()
