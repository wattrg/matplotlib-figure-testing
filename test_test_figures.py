from matplotlib import pyplot as plt
from test_figures import assert_similar_figures, capture_figures
from test_test_figures_runner import run_tests, register_test

@register_test()
def test_line_plot_one_axes_same_plot():
    fig, ax = plt.subplots()
    ax.plot([1,2,3,4], [6,2,5,2])
    ax.plot([2,3,4,5], [7,4,1,2])

    fig2, ax2 = plt.subplots()
    ax2.plot([2,3,4,5], [7,4,1,2])
    ax2.plot([1,2,3,4], [6,2,5,2])

    assert_similar_figures(fig, fig2, ("x_data", "y_data"))

@register_test(should_fail=True)
def test_line_plot_one_axes_dissimilar_plot():
    fig, ax = plt.subplots()
    ax.plot([1,2,3,4], [7,2,5,2])
    ax.plot([2,3,4,5], [7,4,1,2])
    ax.legend(["This line"])

    fig2, ax2 = plt.subplots()
    ax2.plot([2,3,4,5], [7,4,1,2])
    ax2.plot([1,2,3,4], [6,2,5,2])
    ax.legend(["This line"])

    assert_similar_figures(fig, fig2, ("x_data", "y_data"))

@register_test()
def test_pie_similar():
    fig, ax = plt.subplots()
    ax.pie([5, 6, 7, 8])

    fig2, ax2 = plt.subplots()
    ax2.pie([6, 5, 7, 8])

    assert_similar_figures(fig, fig2, ("r", "theta", "center"))

@register_test(should_fail=True)
def test_pie_dissimilar():
    fig, ax = plt.subplots()
    ax.pie([5, 6, 7, 8])

    fig2, ax2 = plt.subplots()
    ax2.pie([6, 6, 7, 8])

    assert_similar_figures(fig, fig2, ("r", "theta", "center"))

@register_test()
def test_bar_similar():
    fig, ax = plt.subplots()
    ax.bar([1, 2, 3], [7, 6, 8])

    fig2, ax2 = plt.subplots()
    ax2.bar([2, 1, 3], [6, 7, 8])

    assert_similar_figures(fig, fig2, ("width", "height"))

@register_test(should_fail=True)
def test_bar_dissimilar():
    fig, ax = plt.subplots()
    ax.bar([1, 2, 3], [5,8,1])

    fig2, ax2 = plt.subplots()
    ax2.bar([1, 2, 3], [6,8,1])

    assert_similar_figures(fig, fig2, ("width", "height"))

@register_test()
def test_scatter_similar():
    fig, ax = plt.subplots()
    ax.scatter([1,2,3,4], [7,4,2,6])
    ax.scatter([2,2,3,4], [8,4,2,6])

    fig2, ax2 = plt.subplots()
    ax2.scatter([2,2,3,4], [8,4,2,6])
    ax2.scatter([1,2,3,4], [7,4,2,6])

    assert_similar_figures(fig, fig2, ("x_data", "y_data"))

@register_test(should_fail=True)
def test_scatter_dissimilar():
    fig, ax = plt.subplots()
    ax.scatter([1,2,3,4], [7,4,2,6])
    ax.scatter([2,2,3,4], [8,4,2,6])

    fig2, ax2 = plt.subplots()
    ax2.scatter([2,2,3,4], [8,4,2,6])
    ax2.scatter([2,2,3,4], [7,4,2,6])

    assert_similar_figures(fig, fig2, ("x_data", "y_data", "marker"))

def plot_data(data1, data2):
    fig1, ax1 = plt.subplots()
    ax1.plot(data1[0], data1[1])

    fig2, ax2 = plt.subplots()
    ax2.plot(data2[0], data2[1])

    plt.show()

@register_test(should_fail=True)
def test_capture_different_figs():
    data = [[1,2,3,4], [2,3,4,5]]
    data2 = [[2,3,4,5], [5,6,7,8]]

    fig1_ref, ax1_ref = plt.subplots()
    ax1_ref.plot(data2[0], data[1])

    fig2_ref, ax2_ref = plt.subplots()
    ax2_ref.plot(data[0], data2[1])
    fig1, fig2 = capture_figures(plot_data, data, data2) 
    assert_similar_figures(fig1, fig1_ref, ("x_data", "y_data"))
    assert_similar_figures(fig2, fig2_ref, ("x_data", "y_data"))

@register_test()
def test_capture_same_figs():
    data = [[1,2,3,4], [2,3,4,5]]
    data2 = [[2,3,4,5], [5,6,7,8]]

    fig1_ref, ax1_ref = plt.subplots()
    ax1_ref.plot(data[0], data[1])

    fig2_ref, ax2_ref = plt.subplots()
    ax2_ref.plot(data2[0], data2[1])

    fig1, fig2 = capture_figures(plot_data, data, data2) 
    assert_similar_figures(fig1, fig1_ref, ("x_data", "y_data"))
    assert_similar_figures(fig2, fig2_ref, ("x_data", "y_data"))

if __name__ == "__main__":
    run_tests()
