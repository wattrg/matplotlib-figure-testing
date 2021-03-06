from matplotlib import pyplot as plt
from test_figures import assert_similar_figures, capture_figures, Figure
from test_test_figures_runner import run_tests, register_test
from test_data.test_figure_repr import test_hist

@register_test()
def test_line_plot_one_axes_same_plot():
    plt.close("all")
    fig, ax = plt.subplots()
    ax.plot([1,2,3,4], [6,2,5,2], c='r')
    ax.plot([2,3,4,5], [7,4,1,2], c='k')

    fig2, ax2 = plt.subplots()
    ax2.plot([2,3,4,5], [7,4,1,2], c='k')
    ax2.plot([1,2,3,4], [6,2,5,2], c='r')

    assert_similar_figures(fig, fig2)

@register_test(should_fail=True)
def test_line_plot_one_axes_dissimilar_plot():
    plt.close("all")
    fig, ax = plt.subplots()
    ax.plot([1,2,3,4], [7,2,5,2])
    ax.plot([2,3,4,5], [7,4,1,2])
    ax.legend(["This line"])

    fig2, ax2 = plt.subplots()
    ax2.plot([2,3,4,5], [7,4,1,2])
    ax2.plot([1,2,3,4], [6,2,5,2])
    ax.legend(["This line"])

    assert_similar_figures(fig, fig2)

@register_test()
def test_line_style():
    plt.close("all")
    fig, ax = plt.subplots()
    ax.plot([1,2,3,4], ls="-")

    fig_ref, ax_ref = plt.subplots()
    ax_ref.plot([1,2,3,4], ls="-")

    assert_similar_figures(fig, fig_ref)

@register_test(should_fail=True)
def test_line_style():
    plt.close("all")
    fig, ax = plt.subplots()
    ax.plot([1,2,3,4], ls="-")

    fig_ref, ax_ref = plt.subplots()
    ax_ref.plot([1,2,3,4], ls=":")

    assert_similar_figures(fig, fig_ref)

@register_test()
def test_pie_similar():
    plt.close("all")
    fig, ax = plt.subplots()
    ax.pie([5, 6, 7, 8])

    fig2, ax2 = plt.subplots()
    ax2.pie([6, 5, 7, 8])

    assert_similar_figures(fig, fig2, ("theta", "r", "patches"))

@register_test(should_fail=True)
def test_pie_dissimilar():
    plt.close("all")
    fig, ax = plt.subplots()
    ax.pie([5, 6, 7, 8])

    fig2, ax2 = plt.subplots()
    ax2.pie([6, 6, 7, 8])

    assert_similar_figures(fig, fig2, ("theta", "r", "patches"))

@register_test()
def test_bar_similar():
    plt.close("all")
    fig, ax = plt.subplots()
    ax.bar([1, 2, 3], [7, 6, 8])

    fig2, ax2 = plt.subplots()
    ax2.bar([2, 1, 3], [6, 7, 8])

    assert_similar_figures(fig, fig2)

@register_test(should_fail=True)
def test_bar_dissimilar():
    plt.close("all")
    fig, ax = plt.subplots()
    ax.bar([1, 2, 3], [5,8,1])

    fig2, ax2 = plt.subplots()
    ax2.bar([1, 2, 3], [6,8,1])

    assert_similar_figures(fig, fig2)

@register_test()
def test_scatter_similar():
    plt.close("all")
    fig, ax = plt.subplots()
    ax.scatter([1,2,3,4], [7,4,2,6])
    ax.scatter([2,2,3,4], [8,4,2,6])

    fig2, ax2 = plt.subplots()
    ax2.scatter([2,2,3,4], [8,4,2,6])
    ax2.scatter([1,2,3,4], [7,4,2,6])

    assert_similar_figures(fig, fig2)

@register_test(should_fail=True)
def test_scatter_dissimilar():
    plt.close("all")
    fig, ax = plt.subplots()
    ax.scatter([1,2,3,4], [7,4,2,6])
    ax.scatter([2,2,3,4], [8,4,2,6])

    fig2, ax2 = plt.subplots()
    ax2.scatter([2,2,3,4], [8,4,2,6])
    ax2.scatter([2,2,3,4], [7,4,2,6])

    assert_similar_figures(fig, fig2)

def plot_data(data1, data2):
    fig1, ax1 = plt.subplots()
    ax1.plot(data1[0], data1[1])

    fig2, ax2 = plt.subplots()
    ax2.plot(data2[0], data2[1])

    plt.show()

@register_test(should_fail=True)
def test_capture_different_figs():
    plt.close("all")
    data = [[1,2,3,4], [2,3,4,5]]
    data2 = [[2,3,4,5], [5,6,7,8]]

    fig1_ref, ax1_ref = plt.subplots()
    ax1_ref.plot(data2[0], data[1])

    fig2_ref, ax2_ref = plt.subplots()
    ax2_ref.plot(data[0], data2[1])
    fig1, fig2 = capture_figures(plot_data, data, data2) 
    assert_similar_figures(fig1, fig1_ref)
    assert_similar_figures(fig2, fig2_ref)

@register_test()
def test_capture_same_figs():
    plt.close("all")
    data = [[1,2,3,4], [2,3,4,5]]
    data2 = [[2,3,4,5], [5,6,7,8]]

    fig1_ref, ax1_ref = plt.subplots()
    ax1_ref.plot(data[0], data[1])

    fig2_ref, ax2_ref = plt.subplots()
    ax2_ref.plot(data2[0], data2[1])

    fig1, fig2 = capture_figures(plot_data, data, data2) 
    assert_similar_figures(fig1, fig1_ref)
    assert_similar_figures(fig2, fig2_ref)

@register_test()
def test_capture_figs_sideeffects():
    plt.close("all")
    fig, ax = plt.subplots()
    original_num_figs = len(plt.get_fignums())
    data = [[1,2,3,4], [2,3,4,5]]
    capture_figures(plot_data, data, data)
    final_num_figs = len(plt.get_fignums())
    assert(final_num_figs == original_num_figs)

@register_test()
def test_repr_similar_figures():
    plt.close("all")
    fig, ax = plt.subplots()
    ax.hist([1, 1, 1 ,2, 2, 3, 4, 5, 5, 5, 5, 6, 6, 7])
    assert_similar_figures(test_hist, fig)

@register_test(should_fail=True)
def test_repr_similar_figures():
    plt.close("all")
    fig, ax = plt.subplots()
    ax.hist([1, 1, 1 ,2, 2, 3, 4, 7, 5, 5, 5, 6, 6, 7])
    assert_similar_figures(test_hist, fig)

@register_test()
def test_sharex():
    plt.close("all")
    fig, (ax1, ax2) = plt.subplots(ncols=2, sharex=True)
    fig2, (ax3, ax4) = plt.subplots(ncols=2, sharex=True)

    assert_similar_figures(fig, fig2)

@register_test(should_fail=True)
def test_sharex_fail():
    plt.close("all")
    fig, (ax1, ax2) = plt.subplots(ncols=2)
    fig2, (ax3, ax4) = plt.subplots(ncols=2, sharex=True)

    assert_similar_figures(fig, fig2)

if __name__ == "__main__":
    plt.ion()
    run_tests()
