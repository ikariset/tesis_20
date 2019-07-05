from classes.RankerTree import RankerTree
from classes.InvertedIndexFactory import InvertedIndexClass
import matplotlib.pyplot as plt


def get_run_process(demo_mode=False):
    _matrix = []
    _docnames = []
    _terms = []

    if demo_mode is False:
        inv_index = InvertedIndexClass("../../../../data/home7/gov2_completa/", "gov2_completa_urls.txt")
    else:
        inv_index = InvertedIndexClass("../../hola/", "dump_10_lineas.txt")

    _matrix, _docnames, _terms = inv_index.get_data_from_collection()

    # RankerTree Object creation
    tree = RankerTree(_matrix,_docnames,_terms)
    tree.unwrapTree()

    # Creating plot for Ordered Matrix
    #tree.getRunsPlotAndData(store_plot=True)

    # Creating plot for Unordered Matrix
    #tree.getRunsPlotAndData(_matrix, store_plot=True)

    tree.getComparisonPlot(data=_matrix, store_plot=True)
    plt.show()


if __name__ == "__main__":
    get_run_process(demo_mode=True)
